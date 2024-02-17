import {createRow} from "./row.ts"
import { invoke } from '@tauri-apps/api/tauri'


let inputText = document.getElementById("input-text") as HTMLTextAreaElement
let button = document.getElementById("classify-button") as HTMLButtonElement
let results = document.getElementById("results") as HTMLDivElement
let upperLimit = document.getElementById("upper-limit") as HTMLInputElement
let lowerLimit = document.getElementById("lower-limit") as HTMLInputElement

let data: JSON

/*check if the input have text, and abilitate it*/
inputText.oninput = () => {
    if (inputText.value.length > 0) {
        button.disabled = false
        button.classList.add("classify-button-animation")
    } else {
        button.disabled = true
        button.classList.remove("classify-button-animation")
    }
}



button.onclick = async () => {

    let upperLimitInt = parseFloat(upperLimit.value)
    let lowerLimitInt = parseFloat(lowerLimit.value)

    if(upperLimitInt>100 || upperLimitInt<0 || lowerLimitInt>100 || lowerLimitInt<0){
        alert("The limits must be between 0 and 100")
        return
    }

    console.log(upperLimitInt)
    console.log(lowerLimitInt)

    let input = inputText.value

    results.innerHTML = ""

    inputText.classList.add("color-red")
    
    

    let link = "http://localhost:8080/predict"+"?text="+input+"&lower_limit="+lowerLimit.value+"&upper_limit="+upperLimit.value

    console.log(link)
    let response = await fetch(link, {
        method: "POST"
    })

 
    if (response.ok) { // if HTTP-status is 200-299
        // get the response body
        inputText.classList.remove("color-red")
        data = await response.json();
        console.log(data);
        //outputText.value = JSON.stringify(data);
    } else {
        console.error("HTTP-Error: " + response.status);
    }


    let map = new Map<number, number>(
        Object.entries(data).map(([key, value]) => [parseInt(key), parseFloat(value)])
        );

    let sortedMap = new Map<number, number>(
        Array.from(map.entries()).sort((a, b) => b[1] - a[1])
        );
    
    console.log(sortedMap)

    for (let [key, value] of sortedMap.entries()) {
        createRow(key, value)
    }
}


window.addEventListener("load", () => {
    startServer()
});


const startServer = async ()=>{
    await invoke('run_server')
    button.disabled = false
}

