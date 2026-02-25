

document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox')
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#submit').onclick=function(event){
      event.preventDefault();
       fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value ,
      body: document.querySelector('#compose-body').value
  })
})
.then(response => response.json())
.then(result => {
    // Print result


 load_mailbox('sent')
});

document.querySelector('#compose-recipients').value = '';
document.querySelector('#compose-subject').value = '';
document.querySelector('#compose-body').value = '';

}


 } //
function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = ``
if (mailbox===`sent`){
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email =>{
           const div = document.createElement('div');
           div.classList.add('email-row');
           div.id = `${email.id}`;
           document.querySelector('#emails-view').append(div)
           const element_email_recipient = document.createElement('div');

            element_email_recipient.classList.add('email_recipient');
            const element_datum = document.createElement('div');
            div.append(element_email_recipient);
            div.append(element_datum);
            const  element_email = document.createElement('div');
            element_email.classList.add('element_email')
            const element_recipient=document.createElement('div');
            element_email_recipient.append(element_email)
            element_email_recipient.append(element_recipient)
          element_email.innerText = email.recipients;
          element_recipient.innerText = email.subject;
          element_datum.innerText = email.timestamp;


          div.addEventListener('click', function(){
         const div1 = document.createElement('div');
         div1.classList.add('email-line');
         div1.innerHTML = `

                          <p><strong>From</strong>: ${email.sender}</p>
                          <p><strong>To</strong>: ${email.recipients}</p>
                          <p><strong>Subject</strong>: ${email.subject}</p>
                          <p><strong>Timestamp</strong>: ${email.timestamp}</p>
                          <button id='reply'>reply</button>
                          <hr>
                          <p>${email.body}</p>`;
                          document.querySelector('#emails-view').innerHTML=``
                          document.querySelector('#emails-view').append(div1)

         div1.querySelector('#reply').onclick = () => {
           alert("clique")
           document.querySelector('#compose-view').style.display = 'block';
           document.querySelector('#emails-view').style.display = 'block';  // cacher la vue emails


};






    // ... do something else with email ...
})}
)});




}else if(mailbox===`inbox`){


fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email =>{
           const div = document.createElement('div');
           div.classList.add(
              'email-row',
              email.read ? 'email-read' : 'email-unread'
            );
           document.querySelector('#emails-view').append(div)
           const element_email_recipient = document.createElement('div');

            element_email_recipient.classList.add('email_recipient');
            const element_datum = document.createElement('div');
            div.append(element_email_recipient);
            div.append(element_datum);
            const  element_email = document.createElement('div');
            element_email.classList.add('element_email')
            const element_recipient=document.createElement('div');
            element_email_recipient.append(element_email)
            element_email_recipient.append(element_recipient)
          element_email.innerText = email.sender;
          element_recipient.innerText = email.subject;
          element_datum.innerText = email.timestamp;


          div.addEventListener('click', function(){

          fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })

         const div1 = document.createElement('div');
         div1.classList.add('email-line');
         div1.innerHTML = `

                          <p><strong>From</strong>: ${email.sender}</p>
                          <p><strong>To</strong>: ${email.recipients}</p>
                          <p><strong>Subject</strong>: ${email.subject}</p>
                          <p><strong>Timestamp</strong>: ${email.timestamp}</p>
                          <button id="reply">reply</button> <button id="archived1">archived</button>
                          <hr>
                          <p>${email.body}</p>`;
                          document.querySelector('#emails-view').innerHTML=``;
                          document.querySelector('#emails-view').append(div1)

         function archiveEmail(email) {
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({ archived: true })
            })
            .then(() => console.log(`Email ${email.id} archivé`));
        }

         div1.querySelector('#archived1').onclick = ()=>{

         archiveEmail(email)
         }


div1.querySelector('#reply').onclick = () => {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'block';

          document.querySelector("#compose-body").value=`Am ${email.timestamp} ${email.sender} wrote \n ${email.body}`;
          document.querySelector(".form-control").value=email.recipients;
            document.querySelector("#compose-recipients").value=email.sender;
            document.querySelector("#compose-subject").value=email.subject;
          document.querySelector('#submit').onclick=function(){
               fetch('/emails', {
                      method: 'POST',
                      body: JSON.stringify({
                      recipients: document.querySelector('#compose-recipients').value,
                      subject: document.querySelector('#compose-subject').value ,
                      body: document.querySelector('#compose-body').value
                  })
                })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result);
                });

                document.querySelector('#compose-recipients').value = '';
                document.querySelector('#compose-subject').value = '';
                document.querySelector('#compose-body').value = '';
                }



};





})
})
})  // Show the mailbox name
}


else{
   fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email =>{
           const div = document.createElement('div');
           div.classList.add('email-row');
           document.querySelector('#emails-view').append(div)
           const element_email_recipient = document.createElement('div');

            element_email_recipient.classList.add('email_recipient');
            const element_datum = document.createElement('div');
            div.append(element_email_recipient);
            div.append(element_datum);
            const  element_email = document.createElement('div');
            element_email.classList.add('element_email')
            const element_recipient=document.createElement('div');
            element_email_recipient.append(element_email)
            element_email_recipient.append(element_recipient)
          element_email.innerText = email.sender;
          element_recipient.innerText = email.subject;
          element_datum.innerText = email.timestamp;


          div.addEventListener('click', function(){
          fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })

         const div1 = document.createElement('div');
         div1.classList.add('email-line');
         div1.innerHTML = `

                          <p><strong>From</strong>: ${email.sender}</p>
                          <p><strong>To</strong>: ${email.recipients}</p>
                          <p><strong>Subject</strong>: ${email.subject}</p>
                          <p><strong>Timestamp</strong>: ${email.timestamp}</p>
                          <button id="reply">reply</button> <button id="unarchived">unarchived</button>
                          <hr>
                          <p>${email.body}</p>`;
                          document.querySelector('#emails-view').innerHTML=``;
                          document.querySelector('#emails-view').append(div1)

         function unarchiveEmail(email) {
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({ archived: false })
            })
            .then(() => console.log(`Email ${email.id} unarchivéd`));
        }

         div1.querySelector('#unarchived').onclick = ()=>{

         unarchiveEmail(email)
         }


})



}

)
  // Show the mailbox name

})

}


 document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

