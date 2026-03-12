let analyzed = false;

setInterval(async () => {

    if(analyzed) return;

    let emailElement = document.querySelector("div.a3s");

    if(!emailElement) return;

    let emailText = emailElement.innerText;

    let senderElement = document.querySelector("span[email]");

    let senderEmail = "";

    if(senderElement){
        senderEmail = senderElement.getAttribute("email");
    }

    let response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
        email_text: emailText,
        sender_email: senderEmail
        })
    });

    let data = await response.json();

    showWarning(data);

    analyzed = true;

}, 4000);


function showWarning(data){

    let banner = document.createElement("div");

    banner.style.background = "#fee2e2";
    banner.style.padding = "12px";
    banner.style.margin = "10px";
    banner.style.border = "1px solid red";
    banner.style.borderRadius = "6px";

    banner.innerHTML =
        "<b>⚠ Email Authenticity Report</b><br>" +
        "Risk Level: " + data.risk_level +
        "<br>Domain Check: " + data.domain_check;

    let emailContainer = document.querySelector("div.a3s");

    if(emailContainer){
        emailContainer.prepend(banner);
    }

}