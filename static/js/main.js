 $(document).ready(function () {
            $('.adminTable').DataTable({
                responsive: true,
            });
     });

$(function(){
    let a = 1;
    $('.icon-div').click(function(){
        $(function(){
            if (a == 1){
                $('.icon-div .fa-solid').removeClass('fa-bars');
                $('.icon-div .fa-solid').addClass('fa-xmark');
                $('.info-div').css('width','250px');
                $('.books-div').css('opacity','1');
                $('.delete-books').css('opacity','1');
                $('.issue-books').css('opacity','1');
                $('.student-books').css('opacity','1');
                $('.sign-div').css('opacity','1');
                $('.login-div').css('opacity','1');
                $('.logout-div').css('opacity','1');
                a = 2;
            }
            else{
                $('.icon-div .fa-solid').removeClass('fa-xmark');
                $('.icon-div .fa-solid').addClass('fa-bars');
                $('.info-div').css('width','0px');
                $('.books-div').css('opacity','0');
                $('.delete-books').css('opacity','0');
                $('.issue-books').css('opacity','0');
                $('.student-books').css('opacity','0');
                $('.sign-div').css('opacity','0');
                $('.login-div').css('opacity','0');
                $('.logout-div').css('opacity','0');
                a = 1;
            }
        });
    });
});



let email = document.getElementById("email-id");
let password = document.getElementById("password-id");
let number = document.getElementById("num");
let lower = document.getElementById("lower");
let upper = document.getElementById("upper");
let letter = document.getElementById("letter");
let message = document.getElementById("message-box");
password.onfocus = function(){
     message.style.display = "flex";
}
password.onblur = function(){
     message.style.display = "none";
}
password.onkeyup = function(){
     let upperCase = /[A-Z]/g;
     if(password.value.match(upperCase)){
        upper.style.color = "Green";
     }
     else{
        upper.style.color = "#C5DFF8";
     }
     let lowerCase = /[a-z]/g;
     if(password.value.match(lowerCase)){
        lower.style.color = "Green";
     }
     else{
        lower.style.color = "#C5DFF8";
     }
     let numberCase = /[0-9]/g;
     if(password.value.match(numberCase)){
        number.style.color = "Green";
     }
     else{
        number.style.color = "#C5DFF8";
     }
     if(password.value.length >= 8){
        letter.style.color = "Green";
     }
     else{
        letter.style.color = "#C5DFF8";
     }
}

