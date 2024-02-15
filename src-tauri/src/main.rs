// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::path::{PathBuf, self};
use std::process::Command;
use std::env;
use std::thread;


// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn run_server(app_handle: tauri::AppHandle){

    let server_handle = thread::spawn(|| {
        let path = path(app_handle);

        // Specify the path to your PowerShell script
        let script_path = path;
    
            // Use Command to spawn a new PowerShell process
            let status = Command::new("powershell")
                .arg("-ExecutionPolicy")
                .arg("Bypass") // Set the execution policy to Bypass
                .arg("-WindowStyle")
                .arg("Hidden") // Imposta lo stile della finestra su Hidden
                .arg("-File")
                .arg(&script_path) // Pass the script path as an argument
                .status()
                .expect("Failed to execute PowerShell script");
    
        // Check the exit status of the PowerShell process
        if status.success() {
            println!("PowerShell script executed successfully");
        } else {
            eprintln!("Error executing PowerShell script");
        }

    });

}


#[tauri::command]
fn path(handle: tauri::AppHandle) -> String {
   let resource_path = handle.path_resolver()
      .resolve_resource("./ai/runner.ps1")
      .expect("failed to resolve resource");

    return resource_path.into_os_string().into_string().unwrap(); 
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![run_server])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
