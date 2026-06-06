const vscode = require('vscode');
const cp = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('YGScript Language Support activated');

    const diagnosticCollection = vscode.languages.createDiagnosticCollection('ygscript');
    context.subscriptions.push(diagnosticCollection);

    // Path to your YGScript interpreter executable
    const compilerPath = "C:\\Users\\Asus\\OneDrive\\Documents\\yusuf\\YGstudio97\\projects\\programe\\ygscript\\bin\\ygscript.exe";

    function checkDocument(document) {
        if (document.languageId !== 'ygscript') {
            return;
        }
        
        // Write current unsaved content to a temporary file
        const text = document.getText();
        const tmpFile = path.join(os.tmpdir(), `ygscript_${Date.now()}.yg`);
        try {
            fs.writeFileSync(tmpFile, text);
        } catch (e) {
            console.error("Failed to write temporary file for checking.");
            return;
        }

        // Run the syntax checker
        cp.exec(`"${compilerPath}" check "${tmpFile}" 2>&1`, (err, stdout, stderr) => {
            try {
                fs.unlinkSync(tmpFile); // Clean up the temp file
            } catch (e) {
                // Ignore cleanup errors
            }
            
            // Remove ANSI colors used in terminal output
            const output = (stdout + '\n' + stderr).replace(/\x1b\[[0-9;]*m/g, ''); 
            const diagnostics = [];

            // Parse error format: [filename:line:col] Error Message
            const regex = /\[.*?\.yg:(\d+):(\d+)\]\s+(.*)/g;
            let match;
            
            while ((match = regex.exec(output)) !== null) {
                const line = Math.max(0, parseInt(match[1], 10) - 1);
                const col = Math.max(0, parseInt(match[2], 10) - 1);
                const message = match[3];

                const range = new vscode.Range(line, col, line, col + 10);
                const diagnostic = new vscode.Diagnostic(range, message, vscode.DiagnosticSeverity.Error);
                diagnostics.push(diagnostic);
            }

            diagnosticCollection.set(document.uri, diagnostics);
        });
    }

    // Command: Run YGScript file
    const runCommand = vscode.commands.registerCommand('ygscript.runFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'ygscript') {
            vscode.window.showErrorMessage('Open a YGScript file first');
            return;
        }

        const filePath = editor.document.fileName;
        const outputChannel = vscode.window.createOutputChannel('YGScript');
        outputChannel.clear();
        outputChannel.show();
        outputChannel.appendLine(`Running: ${filePath}`);
        outputChannel.appendLine('---');

        cp.exec(`"${compilerPath}" run "${filePath}" 2>&1`, (err, stdout, stderr) => {
            outputChannel.appendLine(stdout + stderr);
            if (err) {
                outputChannel.appendLine(`\nExit code: ${err.code}`);
            }
        });
    });

    context.subscriptions.push(runCommand);

    // Debounce typing for real-time checking
    let timeout = undefined;
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            if (timeout) {
                clearTimeout(timeout);
            }
            timeout = setTimeout(() => {
                checkDocument(event.document);
            }, 800);
        })
    );

    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(document => {
            checkDocument(document);
        })
    );
    
    // Check all currently open YGScript files
    vscode.workspace.textDocuments.forEach(doc => checkDocument(doc));
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
