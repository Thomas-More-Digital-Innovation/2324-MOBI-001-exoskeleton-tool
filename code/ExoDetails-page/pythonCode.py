def get_exoskeleton_by_id(exo_id):
    query = """
    MATCH (e:Exo {exoId: $exo_id})
    OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof)-[r2:HAS_DOF]-(j:JointT)
    RETURN e, COLLECT(DISTINCT j.jointTName) AS joints
    """

    exoskeleton_data = g.run(query, exo_id=exo_id).data()

    if exoskeleton_data:
        exoskeleton = exoskeleton_data[0]['e']
        exoskeleton['joints'] = exoskeleton_data[0]['joints']
        return exoskeleton
    else:
        return None

# Route handler for exoskeleton details
@app.route("/exoskeleton/<int:exo_id>")
def exoskeleton_details(exo_id):

    exoskeleton = get_exoskeleton_by_id(exo_id)

    if exoskeleton:
        # Query for the joints of the exoskeleton
        joints_query = """
        MATCH (e:Exo {exoId: $exo_id})-[:HAS_AS_MAIN_DOF]-(d:Dof)-[:HAS_DOF]-(j:JointT)
        RETURN COLLECT(DISTINCT j.jointTName) AS joints
        """

        # Fetch data from Neo4j for joints
        joints_data = g.run(joints_query, exo_id=exo_id).data()

        # Extract the joints from the data
        joints = joints_data[0]['joints'] if joints_data else []


        # Query for exo properties
        properties_query = """
            MATCH (ep:ExoProperty)-[r:HAS_PROPERTY]-(e:Exo {exoId: $exo_id})
            RETURN COLLECT({property: ep.exoPropertyName, value: r.exoPropertyValue}) AS properties
        """

        # Fetch data from Neo4j for properties
        properties_data = g.run(properties_query, exo_id=exo_id).data()

        # Extract the properties from the data
        properties = properties_data[0]['properties'] if properties_data else []

        maingoals_query = """
            MATCH (e:Exo {exoId: $exo_id})-[r:HAS_AIM]-(a)
            CALL {
                WITH r, a
                WITH r, a
                WHERE a:Aim AND r.aimCategory="HAS_AIM_hoofddoel"
                RETURN a.aimName AS maingoal
            
                UNION
            
                WITH r, a
                WITH r, a
                WHERE a:StructureKinematicName AND r.structureKinematicNameCategory="HAS_AIM_hoofddoel"
                RETURN a.structureKinematicNameName AS maingoal
            }
            RETURN e.exoId AS exoId, COLLECT(maingoal) AS maingoals
        """

        # Fetch data from Neo4j for maingoals
        maingoals_data = g.run(maingoals_query, exo_id=exo_id).data()

        # Extract the maingoals from the data
        maingoals = maingoals_data[0]['maingoals'] if maingoals_data else []

        sidegoals_query = """
            MATCH (e:Exo {exoId: $exo_id})-[r:HAS_AIM]-(a)
            CALL {
                WITH r, a
                WITH r, a
                WHERE a:Aim AND r.aimCategory="HAS_AIM_nevendoel"
                RETURN a.aimName AS sidegoal
            
                UNION
            
                WITH r, a
                WITH r, a
                WHERE a:StructureKinematicName AND r.structureKinematicNameCategory="HAS_AIM_nevendoel"
                RETURN a.structureKinematicNameName AS sidegoal
            }
            RETURN e.exoId AS exoId, COLLECT(sidegoal) AS sidegoals
        """

        # Fetch data from Neo4j for sidegoals
        sidegoals_data = g.run(sidegoals_query, exo_id=exo_id).data()

        # Extract the sidegoals from the data
        sidegoals = sidegoals_data[0]['sidegoals'] if sidegoals_data else []

        # Query for contraindications
        contraindications_query = """
            MATCH (e:Exo {exoId: $exo_id})-[r:DOESNT_GO_WITH]-(a)
            CALL {
                WITH r, a
                WITH r, a
                WHERE a:Aim
                RETURN a.aimName AS contraindication
            
                UNION
            
                WITH r, a
                WITH r, a
                WHERE a:StructureKinematicName
                RETURN a.structureKinematicNameName AS contraindication
            }
            RETURN e.exoId AS exoId, COLLECT(contraindication) AS contraindications
        """

        # Fetch data from Neo4j for contraindications
        contraindications_data = g.run(contraindications_query, exo_id=exo_id).data()

        # Extract the contraindications from the data
        contraindications = contraindications_data[0]['contraindications'] if contraindications_data else []

        # Professional activities main activity query
        pa_hoofdoelen_query = """
            MATCH (e:Exo {exoId: $exo_id})-[r1:HAS_AIM]-(a)-[r2]-(ao:AndObjectAimSKN)-[r3:HAS_AND_OBJECT_AIM_SKN]-(aoa:AnalysisOfActivity)-[r4:ANALYSES_ACTIVITY]-(ac:Activity)
            CALL {
                WITH r1, a, ac
                WITH r1, a, ac
                WHERE a:Aim AND r1.aimCategory = "HAS_AIM_hoofddoel"
                RETURN ac.activityDescription  AS mainActivity

                UNION

                WITH r1, a, ac
                WITH r1, a, ac
                WHERE a:StructureKinematicName AND r1.structureKinematicNameCategory="HAS_AIM_hoofddoel"
                RETURN ac.activityDescription AS mainActivity
            }
            RETURN e.exoId AS exoId, COLLECT(DISTINCT mainActivity) AS mainActivities
        """

        # Fetch data from Neo4j for hoofdoelen
        hoofdoelen_data = g.run(pa_hoofdoelen_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        main_activities = hoofdoelen_data[0]['mainActivities'] if hoofdoelen_data else []

        pa_nevendoelen_query = """
            match (e:Exo {exoId: $exo_id})-[r1:HAS_AIM]-(a)-[r2]-(ao:AndObjectAimSKN)-[r3:HAS_AND_OBJECT_AIM_SKN]-(aoa:AnalysisOfActivity)-[r4:ANALYSES_ACTIVITY]-(ac:Activity)
            call {
                with r1, a, ac
                with r1, a, ac
                where a:Aim and r1.aimCategory = "HAS_AIM_nevendoel"
                return ac.activityDescription as sideActivity
            
                union
            
                with r1, a, ac
                with r1, a, ac
                where a:StructureKinematicName and r1.structureKinematicNameCategory="HAS_AIM_nevendoel"
                return ac.activityDescription as sideActivity
            }
            return e.exoId as exoId, collect (DISTINCT sideActivity) AS sideActivities;
        """

        # Fetch data from Neo4j for hoofdoelen
        nevendoelen_data = g.run(pa_nevendoelen_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        side_activities = nevendoelen_data[0]['sideActivities'] if nevendoelen_data else []

        houdingsondersteuning_bij_query = """
            match (e:Exo {exoId: $exo_id})-[r:GIVES_POSTURAL_SUPPORT_IN]-(d:Dof) 
            where r.aim="Ja" and r.mechanism IN ["door momentenevenwicht", "door klik"]
            call {
                with r, d
                with r, d
                where r.direction=1
                return d.namePos as dof
            
                union
            
                with r, d
                with r, d
                where r.direction=-1
                return d.nameNeg as dof
            }
            return e.exoId, collect(DISTINCT dof) as dofs;
        """

        # Fetch data from Neo4j for hoofdoelen
        houdingsondersteuning_bij_data = g.run(houdingsondersteuning_bij_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        houdingsondersteuning_bij = houdingsondersteuning_bij_data[0]['dofs'] if houdingsondersteuning_bij_data else []
    
        houdingsondersteuning_door_query = """
            match (e:Exo {exoId: $exo_id})-[r:GIVES_POSTURAL_SUPPORT_IN]-(d:Dof) 
            where r.aim="Ja" and r.mechanism IN ["door blokkage"]
            call {
                with r, d
                with r, d
                where r.direction=1
                return d.namePos as dof
            
                union
            
                with r, d
                with r, d
                where r.direction=-1
                return d.nameNeg as dof
            }
            return e.exoId as exoId, collect(DISTINCT dof) as dofs;
        """

        # Fetch data from Neo4j for hoofdoelen
        houdingsondersteuning_door_data = g.run(houdingsondersteuning_door_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        houdingsondersteuning_door = houdingsondersteuning_door_data[0]['dofs'] if houdingsondersteuning_door_data else []
        
        limiteert_query = """
            match (e:Exo {exoId: $exo_id})-[r:LIMITS_IN]-(d:Dof) 
            where r.aim="Nee"
            call {
                with r, d
                with r, d
                where r.direction=1
                return d.namePos as dof
            
                union
            
                with r, d
                with r, d
                where r.direction=-1
                return d.nameNeg as dof
            }
            return e.exoId as exoId, collect(DISTINCT dof) as dofs;
        """

        # Fetch data from Neo4j for hoofdoelen
        limiteert_data = g.run(limiteert_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        limiteert = limiteert_data[0]['dofs'] if limiteert_data else []

        vergemakkelijkt_query = """
            match (e:Exo {exoId: $exo_id})-[r:ASSISTS_IN]-(d:Dof) 
            where r.aim="Ja" 
            call {
                with r, d
                with r, d
                where r.direction=1
                return d.namePos as dof
            
                union
            
                with r, d
                with r, d
                where r.direction=-1
                return d.nameNeg as dof
            }
            return e.exoId as exoId, collect(DISTINCT dof) as dofs;
        """

        # Fetch data from Neo4j for hoofdoelen
        vergemakkelijkt_data = g.run(vergemakkelijkt_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        vergemakkelijkt = vergemakkelijkt_data[0]['dofs'] if vergemakkelijkt_data else []

        fromPart_query = """
            match (e:Exo {exoId: $exo_id})-[r1:TRANSFERS_FORCES_FROM]-(p1:Part)
            return e.exoId, p1.partName as fromPart
        """

        fromPart_data = g.run(fromPart_query, exo_id=exo_id).data()

        fromPart = fromPart_data[0]['fromPart'] if fromPart_data else []

        toPart_query = """
            match (e:Exo {exoId: $exo_id})-[r2:TRANSFERS_FORCES_TO]-(p2:Part)
            return e.exoId, p2.partName as toPart;
        """

        toPart_data = g.run(toPart_query, exo_id=exo_id).data()

        toPart = toPart_data[0]['toPart'] if toPart_data else []

        weerstand_bij_query = """
            match (e:Exo)-[r:GIVES_RESISTANCE_IN]-(d:Dof) 
            where r.aim="Ja"
            call {
                with r, d
                with r, d
                where r.direction=1
                return d.namePos as dof
            
                union
            
                with r, d
                with r, d
                where r.direction=-1
                return d.nameNeg as dof
            }
            return e.exoId as exoId, collect(DISTINCT dof) as dofs;
        """

        # Fetch data from Neo4j for hoofdoelen
        weerstand_bij_data = g.run(weerstand_bij_query, exo_id=exo_id).data()

        # Extract the hoofdoelen from the data
        weerstand_bij = weerstand_bij_data[0]['dofs'] if weerstand_bij_data else []

        hindert_query = """
            match (e:Exo)-[r:DISCOMFORTS_IN]-(d:Dof) 
            call {
                with r, d
                with r, d
                where r.direction=1
                return d.namePos as dof
            
                union
            
                with r, d
                with r, d
                where r.direction=-1
                return d.nameNeg as dof
            }
            return e.exoId as exoId, collect(DISTINCT dof) as dofs;
        """

        # Fetch data from Neo4j for hoofdoelen
        hindert_data = g.run(hindert_query, exo_id=exo_id).data()
        
        # Extract the hoofdoelen from the data
        hindert = hindert_data[0]['dofs'] if hindert_data else []
    
        return render_template(
            "exoskeleton_details.html",
            exoskeleton=exoskeleton,
            joints=joints,
            properties=properties,
            maingoals=maingoals,
            sidegoals=sidegoals,
            contraindications=contraindications,
            main_activities=main_activities,
            side_activities=side_activities,
            houdingsondersteuning_bij=houdingsondersteuning_bij,
            houdingsondersteuning_door=houdingsondersteuning_door,
            limiteert=limiteert,
            vergemakkelijkt=vergemakkelijkt,
            fromPart=fromPart,
            toPart=toPart,
            weerstand_bij=weerstand_bij,
            hindert=hindert,
        )
    else:
        return "Exoskeleton not found", 404