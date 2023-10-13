# Troubleshooting Document: PowerShell Script Execution Policy Error

## Issue

You encounter the following error when trying to activate a virtual environment or run a script in PowerShell:

```
.\venv\Scripts\activate : File D:\Repos\sense2exion\code\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies.
```

## Solution

### 1. Open PowerShell as an Administrator

   - Click the Windows Start button.
   - Type "PowerShell."
   - Right-click on "Windows PowerShell" and select "Run as administrator."

### 2. Check Your Current Execution Policy

In PowerShell, you can check your current execution policy using the following command:

```powershell
Get-ExecutionPolicy
```

### 3. Change the Execution Policy

If your current execution policy is "Restricted" or another policy that's blocking script execution, you can change it to "RemoteSigned" or another appropriate policy. "RemoteSigned" allows you to run scripts that you've created or obtained locally without requiring a digital signature.

To set the execution policy to "RemoteSigned," use the following command:

```powershell
Set-ExecutionPolicy RemoteSigned
```

If you're working in a restricted environment and need to run unsigned scripts, you can set the execution policy to "Unrestricted" (though it's less secure):

```powershell
Set-ExecutionPolicy Unrestricted
```

### 4. Confirm the Change

PowerShell will ask for confirmation. Type "Y" and press Enter to confirm the change.

### 5. Run the Activation Script

After you've changed the execution policy, try running the activation script again.

### 6. Revert the Execution Policy (Optional)

Once you're done, if you want to revert your execution policy to its previous state (for security reasons), you can set it back to its original value.

Remember that changing the execution policy may introduce security risks, so it's essential to understand the implications and make changes accordingly based on your specific needs and security concerns.
