// JS checks correct fields are inputed in the login and registration forms

// Login Verification
$('#userlogin').on('submit', function(evt) {
    
    var uname = $('#uname').val();
    var pwd = $('#pwd').val();
    var letterNumber = /^[0-9a-zA-Z]+$/;

    if (uname.match(letterNumber) || pwd.match(letterNumber)) {
        return true;
    } else {
        alert("Invalid input");
        evt.preventDefault();
    }
});

// Registration Verification
$('#registration').on('submit', function(evt) {
    
    var uname = $('#uname').val();
    var fname = $('#fname').val();
    var lname = $('#lname').val();
    var email = $('#email').val();
    var pwd = $('#pwd').val();
    var letterNumber = /^[0-9a-zA-Z]+$/;

    if (uname.match(letterNumber) || fname.match(letterNumber) ||
        lname.match(letterNumber) || email.match(letterNumber) ||
        pwd.match(letterNumber)) {
        return true;
    } else {
        alert("Invalid input");
        evt.preventDefault();
    }
});
