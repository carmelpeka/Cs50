document.addEventListener('DOMContentLoaded', function() {

const dash=document.getElementById('dashboard')
 const bouton =  document.getElementById('plot_button')
if(dash){
    if(bouton){
           bouton.addEventListener("click",(e)=>{
           e.preventDefault();
           let begin_day =document.getElementById('id_begin_day').value;
           let period =document.getElementById('id_period').value;

            let begin_month = document.getElementById('id_begin_month').value;

            let begin_year =document.getElementById('id_begin_year').value;
            let begin_date_str = `${begin_year}-${begin_month.toString().padStart(2,'0')}-${begin_day .toString().padStart(2,'0')}`;

    // Récupérer End
            let end_day = document.getElementById('id_end_day').value;
            let end_month = document.getElementById('id_end_month').value;
            let end_year = document.getElementById('id_end_year').value;
            let end_date_str = `${end_year}-${end_month.toString().padStart(2,'0')}-${end_day.toString().padStart(2,'0')}`;

            const csrftoken = document.querySelector('meta[name="csrf-token"]').content;
            fetch(`/dashboard`, {
                                      method: 'POST',
                                      headers: {
                                       "Content-Type": "application/json",
                                      "X-CSRFToken": csrftoken },
                                      body: JSON.stringify({
                                     begin:begin_date_str,
                                     end: end_date_str,
                                     period:period,


                                                  })
                                                  })
                                                  .then(response => response.json())
                                                  .then(dict =>{
                                                  console.log(dict)
                                                   createChart("myChart1", "line", dict["label"],dict["data"],"global amount")
                                                   createChart("myChart2", "bar", dict["labels_income"], dict["data_income"], "income")
                                                   createChart("myChart3", "bar", dict["labels_expense"], dict["data_expense"], "expense")


})
})
}

}


// Objet global pour stocker les graphiques
const charts = {};

function createChart(canvasId, type, labels, data, label) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    // Détruire l'ancien graphique s'il existe
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    // Créer le nouveau graphique
    charts[canvasId] = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}











})

