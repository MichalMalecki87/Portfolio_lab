document.addEventListener("DOMContentLoaded", function() {
    let donations = document.querySelectorAll('field-__str__')
    donations.forEach(donation => {
        if (donation.innerText.includes('już odebrany')) {
            donation.style.color = 'grey'
        }
    })
    console.log(donations)
})