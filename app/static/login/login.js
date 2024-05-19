console.log("hello world");


document.getElementById('get-started').addEventListener('click', function() {
    document.querySelector('.welcome-container').classList.toggle('none');
    document.querySelector('.login').classList.toggle('block');
});

/*===== LOGIN SHOW and HIDDEN =====*/
const signUp = document.getElementById('sign-up'),
    signIn = document.getElementById('sign-in'),
    loginIn = document.getElementById('login-in'),
    loginUp = document.getElementById('login-up')


signUp.addEventListener('click', ()=>{
    // Remove classes first if they exist
    loginIn.classList.remove('block')
    loginUp.classList.remove('none')

    // Add classes
    loginIn.classList.toggle('none')
    loginUp.classList.toggle('block')
})

signIn.addEventListener('click', ()=>{
    // Remove classes first if they exist
    loginIn.classList.remove('none')
    loginUp.classList.remove('block')

    // Add classes
    loginIn.classList.toggle('block')
    loginUp.classList.toggle('none')
})

// Close Button Functionality for Flash Messages
document.querySelectorAll('.flash-message .close-btn').forEach(button => {
    button.addEventListener('click', function() {
        const flashMessage = this.parentElement;
        flashMessage.classList.add('hide');
        setTimeout(() => {
            flashMessage.remove();
        }, 300); // Match the transition duration
    });
});
