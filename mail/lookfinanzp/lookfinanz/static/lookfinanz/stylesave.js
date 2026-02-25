document.addEventListener('DOMContentLoaded', function() {

  if (document.getElementById('newtransaction')) {
    const select = document.getElementById("transaction_type");
    if (select){
    select.addEventListener("change", () => {
        let category = []
       if (select.value === 'income') {
          category = INCOME_CATEGORY_CHOICES
        } else if (select.value === 'expense') {
          category = EXPENSE_CATEGORY_CHOICES
        }
    const select2 = document.getElementById("category")
    select2.innerText=""
    category.forEach(cat => {
    const option = document.createElement('option'); //
    option.value = cat[0];                            //
    option.innerText = cat[1];                        //
    select2.appendChild(option);                       //
});

    })};
    const simulate =document.getElementById("simulate")
    if (simulate){

    simulate.addEventListener("click",(event)=>{
    event.preventDefault()
    n=document.querySelector("#simulate_number").value

    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;
    fetch(`/random_data_upload`, {
      method: 'POST',
      headers: {
       "Content-Type": "application/json",
      "X-CSRFToken": csrftoken },
      body: JSON.stringify({
      number:n
                  })
        })

    })
    }
  }

 if (document.getElementById('alltransaction')){
  const select =document.getElementById('transaction_type_index')
  if(select){
  select.addEventListener("change", () => {
        let category = []
       if (select.value === 'income') {
          category = INCOME_CATEGORY_CHOICES
        } else if (select.value === 'expense') {
          category = EXPENSE_CATEGORY_CHOICES
        }
    const select2 = document.getElementById("category_index")
    select2.innerText=""
    category.forEach(cat => {
    const option = document.createElement('option'); //
    option.value = cat[0];                            //
    option.innerText = cat[1];                        //
    select2.appendChild(option);                       //
});

    })



  }

const select3=document.getElementById("filter_button")
if(select3){
    select3.addEventListener("click",(e)=>{
           e.preventDefault();
           let cat=document.getElementById("category_index").value

           let type=document.getElementById('transaction_type_index').value
           let begin_day = document.getElementById('id_begin_day').value;

            let begin_month = document.getElementById('id_begin_month').value;

            let begin_year = document.getElementById('id_begin_year').value;
            let begin_date_str = `${begin_year}-${begin_month.toString().padStart(2,'0')}-${begin_day .toString().padStart(2,'0')}`;

    // Récupérer End
            let end_day = document.getElementById('id_end_day').value;
            let end_month = document.getElementById('id_end_month').value;
            let end_year = document.getElementById('id_end_year').value;
            let end_date_str = `${end_year}-${end_month.toString().padStart(2,'0')}-${end_day.toString().padStart(2,'0')}`;


// Exemple : "2026-01-23"
           const csrftoken = document.querySelector('meta[name="csrf-token"]').content;
            fetch(`/filter_data_of_index_page`, {
              method: 'POST',
              headers: {
               "Content-Type": "application/json",
              "X-CSRFToken": csrftoken },
              body: JSON.stringify({
              category:cat,
              begin:begin_date_str,
              end:end_date_str,
              transaction_type:type
                          })
                })
                .then(response => response.json())
                .then(list_dict =>{
                const foundation=document.getElementById("transaction_select_filter_oder_all")
                foundation.innerHTML = ""
                list_dict.forEach((dict)=>{
                    const div1 = document.createElement('div');
                    div1.classList.add('card');
                    foundation.append(div1)
                    const div2 = document.createElement('div');
                    div2.classList.add('transaction_inline');
                    div1.append(div2)
                    const div3 = document.createElement('div');
                    div3.innerHTML= `<p>${dict["name"]}</p>`;
                    div2.append(div3)
                    const div4 = document.createElement('div');
                    div4.innerHTML= `<p>${dict["description"]}</p>`;
                    div2.append(div4)
                    const div5 = document.createElement('div');
                    if(dict["transaction_type"]=="income"){
                    div5.innerHTML= `<p style="color: green;">${dict["amount"]}</p>`;
                    }else{
                    div5.innerHTML= `<p style="color: red;">-${dict["amount"]}</p>`;
                    }
                    div2.append(div5)
                    const div6 = document.createElement('div');
                    div6.innerHTML= `<p>${dict["transaction_type"]}</p>`;
                    div2.append(div6)
                    const div7 = document.createElement('div');
                    div7.innerHTML= `<p>${dict["category"]}</p>`;
                    div2.append(div7)
                    const div8 = document.createElement('div');
                    div8.innerHTML= `<p>${dict["date"]}</p>`;
                    div2.append(div8)
                    div1.addEventListener('dblclick', function(e) {
                        e.preventDefault()
                        div1.innerHTML= `<form >
                                          <div>
                                            <label for="name">Name</label>
                                            <input type="text" id="name" name="name" >
                                          </div>

                                          <div>
                                            <label for="description">Description</label>
                                            <input type="text" id="description" name="description" >
                                          </div>

                                          <div>
                                            <label for="amount">Amount</label>
                                            <input type="number" id="amount" name="amount" >
                                          </div>

                                          <div>
                                            <label for="transaction_type">Type </label>
                                            <input type="text" id="transaction_type" name="transaction_type" >
                                          </div>

                                          <div>
                                            <label for="category">Catégorie</label>
                                            <input type="text" id="category" name="category" >
                                          </div>

                                          <!-- Boutons -->
                                          <div style="margin-top: 15px;">
                                            <button type="button" id="button_delete_transaction" name="action" value="delete">Delete</button>
                                            <button type="button" id="save_modify_transaction" name="action" value="save" style="margin-left: 10px; color: red;">Save</button>
                                          </div>
                                        </form>
                                        `;
                                      div1.querySelector('#name').value = dict['name'];
                                      div1.querySelector('#description').value = dict['description'];
                                      div1.querySelector('#amount').value = dict['amount'];
                                      div1.querySelector('#transaction_type').value = dict['transaction_type'];
                                      div1.querySelector('#category').value = dict['category'];
                                     const btn = div1.querySelector("#button_delete_transaction");

                                     console.log(dict["id"])
                                    btn.addEventListener('click',()=>{
                                     console.log(dict["id"])

                                    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;
                                    fetch(`/delete_transaction`, {
                                      method: 'PUT',
                                      headers: {
                                       "Content-Type": "application/json",
                                      "X-CSRFToken": csrftoken },
                                      body: JSON.stringify({
                                     id:dict["id"]
                                                  })
                                                  })
                                                  .then(response => response.json())
                                                  .then(list_dict =>{alert(list_dict["message"])})
                                   div1.remove()
                    })
                    const btn2 = div1.querySelector("#save_modify_transaction");
                     btn2.addEventListener('click',()=>{

                              let   name=     div1.querySelector('#name').value
                              let   description=     div1.querySelector('#description').value
                               let   amount=    div1.querySelector('#amount').value
                                let   type=   div1.querySelector('#transaction_type').value
                                 let  category=   div1.querySelector('#category').value

                    const div1_ = document.createElement('div');
                    div1_.classList.add('card');
                    const div2_ = document.createElement('div');
                    div2_.classList.add('transaction_inline');
                    div1_.append(div2_)
                    const div3_ = document.createElement('div');
                    div3_.innerHTML= `<p>${name}</p>`;
                    div2_.append(div3_)
                    const div4_ = document.createElement('div');
                    div4_.innerHTML= `<p>${description}</p>`;
                    div2_.append(div4_)
                    const div5_ = document.createElement('div');
                    if(type =="income"){
                    div5_.innerHTML= `<p style="color: green;">${amount}</p>`;
                    }else{
                    div5_.innerHTML= `<p style="color: red;">-${amount}</p>`;
                    }
                    div2_.append(div5_)
                    const div6_ = document.createElement('div');
                    div6_.innerHTML= `<p>${type}</p>`;
                    div2_.append(div6_)
                    const div7_ = document.createElement('div');
                    div7_.innerHTML= `<p>${category}</p>`;
                    div2_.append(div7_)
                    const div8_ = document.createElement('div');
                    div8_.innerHTML= `<p>${dict["date"]}</p>`;
                    div2_.append(div8_)
                    div1.innerHTML=div1_.innerHTML
                    fetch(`/update_transaction`, {
                                      method: 'PUT',
                                      headers: {
                                       "Content-Type": "application/json",
                                      "X-CSRFToken": csrftoken },
                                      body: JSON.stringify({
                                     id:dict["id"],
                                     name:name,
                                     description:description,
                                     amount:amount,
                                     type:type,
                                     category:category
                                                  })
                                                  })
                                                  .then(response => response.json())
                                                  .then(list_dict =>{alert(list_dict["message"])})



                     })





                    })

                })
                })

    })
}






 }




}); // <-- attention à cette accolade et au point-virgule

const EXPENSE_CATEGORY_CHOICES = [
    ['rent', 'Rent'],
    ['food', 'Food'],
    ['transport', 'Transport'],
    ['health', 'Health'],
    ['entertainment', 'Entertainment'],
    ['education', 'Education'],
    ['bills', 'Bills'],
    ['shopping', 'Shopping'],
    ['taxes', 'Taxes'],
];

const INCOME_CATEGORY_CHOICES = [
    ['salary', 'Salary'],
    ['freelance', 'Freelance'],
    ['interest', 'Interest'],
    ['dividends', 'Dividends'],
    ['gifts', 'Gifts'],
];




  ; // "income" ou "expense"

