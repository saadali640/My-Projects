document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  document.querySelector("#compose-form").addEventListener("submit", send_mail)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function email_view(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'block'; 
  
      // ... do something else with email ...

      document.querySelector('#email-view').innerHTML = `
       <h4>From: ${email.sender}</h4>
       <h5>To: ${email.recipients}</h5>
       <h6>Subject: ${email.subject}</h6>
       <h6>Date: ${email.timestamp}</h6>
       <button class="button-8" id="button-8">Reply</button>
       <hr>
       <p>${email.body}</p>
   `

   
  const rplbtn = document.querySelector('#button-8');
  rplbtn.addEventListener("click", function() {compose_email();
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.split(" ",1)[0] != "Re:"){email.subject = "Re: " + email.subject;}
    document.querySelector('#compose-subject').value = email.subject;
    document.querySelector('#compose-body').value = " On " + email.timestamp +" "+ email.sender + " wrote: " + email.body;
  
  });
  });


  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}


function archive_email(id, archived){
  const archivedStatus = !archived;
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archivedStatus
    })
  })
  load_mailbox("index");
  window.location.reload();
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


fetch(`/emails/${mailbox}`)
.then(response => response.json())
.then(emails => {

    // ... do something else with emails ...
    emails.forEach(perEmail => {


    const emailLi = document.createElement('div');
    emailLi.innerHTML = `
     <h5>${perEmail.sender}</h5>
     <h6 style="margin-left: 17px; margin-top: 4px;">${perEmail.subject}</h6>
     <h6 style="margin-left: auto; margin-top: 5px; margin-right: 10px;">${perEmail.timestamp}</h6>

    `;

    emailLi.className = perEmail.read ? "read": "un";

    emailLi.addEventListener('click', function() {email_view(perEmail.id)});

    document.querySelector('#emails-view').append(emailLi);

    if (mailbox !== "sent") {
      const button = document.createElement("button");
      if (mailbox == "archive"){
        button.innerHTML = `Unarchive`;}
      else{
        button.innerHTML = `Archive`;}  
      button.className = "button-8";
      emailLi.append(button);
      button.addEventListener("click", function() {archive_email(perEmail.id, perEmail.archived)});
    }

   });
   })
}



function send_mail(event){
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
  })
})

.then(response => response.json())
.then(result => {
    // Print result
    console.log(result);
    load_mailbox("sent");
});
}


