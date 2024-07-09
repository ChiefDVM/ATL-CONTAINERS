
const Req = async (cars) => {
    const response = await axios.get('/requestCombinations', {
        params: {
            "cars": cars
        }
    })
    return response.data
}

document.querySelector('.submitCar').addEventListener('click', function () {

    const params = new URLSearchParams();
    addedCars.forEach((value, index) => {
        params.append(`array[${index}]`, value);
    })

    axios.get('/requestCombinations', {
        params: params
    })
        .then(function (response) {
            console.log('Array sent successfully:', response.data.Answer);
            const answer = response.data.Answer;
            renderTable(answer)
        })
        .catch(function (error) {
            console.error('Error sending array:', error);
        });
})

function renderTable(answer) {
    const title = document.querySelector('.titleComb')
    title.innerHTML = ''
    
    if (title) {
        console.log("hahs")
        const titleText = document.createElement("h2");
        titleText.innerHTML = 'Car Combinations';
        title.appendChild(titleText);
    } else {
        console.error('Element with class "title" not found');
    }
    const containerDiv = document.getElementById('container');
    containerDiv.innerHTML = ''; 
    

    if(answer !== 0){
        if(document.querySelector('.noSolution')){
            document.querySelector('.noSolution').remove();
        }
        answer.forEach((caseData, caseIndex) => {
            const caseSection = document.createElement('div');
            
            caseSection.innerHTML = `<h2>Case ${caseIndex + 1}</h2><h3>No. of Containers: ${caseData.Found.length}</h3>`;
    
            
            const table = document.createElement('table');
            table.classList.add('table', 'containersTable');
    

            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr class="table-secondary">
                    <th scope="col">S.No.</th>
                    <th scope="col">Containers</th>
                    <th scope="col">No. of Cars</th>
                    <th scope="col">Vanning Date</th>
                    <th scope="col">Yard</th>
                </tr>
            `;
            table.appendChild(thead);
    

            const tbody = document.createElement('tbody');
            caseData.Found.forEach((containerInfo, containerIndex) => {
                const tr = document.createElement('tr');
                tr.classList.add('table-success');
                tr.innerHTML = `
                    <th scope="row">${containerIndex + 1}</th>
                    <td>${containerInfo.Container}</td>
                    <td>${containerInfo.Container.length}</td>
                    <td>${containerInfo.VanningDate}</td>
                    <td>${containerInfo.Yard}</td>
                `;
                tbody.appendChild(tr);
                
            });

            table.appendChild(tbody);
    
            caseSection.appendChild(table);

            
            if(caseData.NotFound.length != 0){
                const notFound = document.createElement('div');
                notFound.innerHTML = `<h4><span style="color: red;">Not in Container: </span>${caseData.NotFound}</h4>`;
                caseSection.appendChild(notFound);
            }
            
    
            containerDiv.appendChild(caseSection);
        });
    } 
    else{
        if(document.querySelector('.noSolution')){
            document.querySelector('.noSolution').remove();
        }
        const noSolution = document.createElement('div');
        noSolution.classList.add('noSolution')
        noSolution.innerHTML = ''; 
        const caseSection = document.createElement('div');
        caseSection.innerHTML = `<h2>NO RESULT FOUND</h2>`;
        noSolution.appendChild(caseSection)
        containerDiv.parentNode.insertBefore(noSolution, containerDiv.nextSibling)
    }
}