export function createRow(chiave:number,valore:any) {

    let topics = ["Society & culture", "Science & Mathematics", "Health", "Education & Reference", "Computers & Internet", "Sports", "Business & Finance", "Entertainment & Music", "Family & Relationships", "Politics & Government"]



    let div = document.getElementById("results") as HTMLDivElement       // elemento dove verrà inserito il risultato

    /*
        <div class="result">
          <div class="topic">Topic</div>
          <div class="confidence">Confidence</div>
        </div>
    */

    let row = document.createElement("div") as HTMLDivElement
    row.className = "row"

    let result = document.createElement("div") as HTMLDivElement
    result.className = "result"

    let topicDiv = document.createElement("div") as HTMLDivElement
    topicDiv.className = "topic"

    let confidence = document.createElement("div") as HTMLDivElement
    confidence.className = "confidence"

    result.appendChild(topicDiv)               // aggiungo i due elementi al div result
    result.appendChild(confidence)

    row.appendChild(result)                 // aggiungo il div result al div row
    div.appendChild(row)                    // aggiungo il div row al div results

    let topic = topics[chiave]

    // ora manipolo i dati e li inserisco nei div
    topicDiv.innerText = topic + ":"
    confidence.innerText = valore + "%"

}