var id_ma_cay = document.getElementById("id_ma_cay"),
uusermsg = document.getElementById("uname_error_ma");
function checkusername(){
    var error = "";
    var charReg = /^\s*[a-zA-Z0-9,\s]+\s*$/;
    
    if(id_ma_cay.value){ // field are filled, let's validate
        var inputVal = id_ma_cay.value;
        if (!charReg.test(inputVal)) {
            error = "Error: Username không chấp nhập các chữ số đặt biệt!";
        }
        // //check if either value contains any numbers
        // if(/[0-9]/.test(id_ma_cay.value))
        //     error = "Error: Username không chấp nhập chữ số!";
        //     //check if either value contains any characters besides words and hyphens
        // else {
        //     var inputVal = id_ma_cay.value;
        //     if (!charReg.test(inputVal)) {
        //         error = "Error: Username không chấp nhập các chữ số đặt biệt!";
        //     }
        // }
    }
    else error = "Error: Hãy nhập Username!";

    if(error) {
        uusermsg.innerHTML = error;
        document.getElementById('save').disabled = true;
        document.getElementById('usave').disabled = true;
    }
    else {
        uusermsg.innerHTML = "";
        document.getElementById('save').disabled = false;
        document.getElementById('usave').disabled = false;
    }
}

id_ma_cay.onchange = checkusername;

var specialChars = "<>@!#$%^&*()_+[]{}?:;|'\"\\,./~`-=";
var checkForSpecialChar = function(string){
    for(i = 0; i < specialChars.length;i++){
      if(string.indexOf(specialChars[i]) > -1){
          return true
       }
    }
    return false;
}

// var str = "YourText";
// if(checkForSpecialChar(str)){
//      alert("Not Valid");
// } else {
//        alert("Valid");
// }

var ufname = document.getElementById("id_first_name"),
ulname = document.getElementById("id_last_name"),
umsg = document.getElementById("uname_error_msg");
var format = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
function checkfullname(){
    var error = "";
    umsg.innerHTML = error;
    if(ufname.value && ulname.value){ // both fields are filled, let's validate
        //check if either value contains any numbers
        if(/[0-9]/.test(ufname.value) || /[0-9]/.test(ulname.value)) 
            error = "Error: Họ tên không chấp nhập chữ số!";
            //check if either value contains any characters besides words and hyphens
        else {
            var inputVal = ufname.value + " " + ulname.value;
            inputVal = removeAscent(inputVal)
            if (format.test(inputVal))
                error = "Error: Họ tên không chấp nhập các chữ số đặt biệt!";
        }
    }
    else if(ufname.value) // means lname is empty
        error = "Error: Tên không để trống!";
    else if(ulname.value) // means fname is empty
        error = "Error: Họ và tên lót không để trống!";
    else //both are empty
        error = "Error: Hãy nhập đầy đủ họ tên!";

    if(error) {
        umsg.innerHTML = error;
        document.getElementById('save').disabled = true;
        document.getElementById('usave').disabled = true;
    }
    else {
        umsg.innerHTML = "";
        document.getElementById('save').disabled = false;
        document.getElementById('usave').disabled = false;
    }
}

ufname.onchange = checkfullname;
ulname.onchange = checkfullname;

$("#id_email").keyup(function(){

    var email = $("#id_email").val();
    document.getElementById('uname_error_email').innerHTML = '';
    if(email != 0)
    {
        if(isValidEmailAddress(email))
        {
          document.getElementById('uname_error_email').innerHTML = '';
          document.getElementById('save').disabled = false;
          document.getElementById('usave').disabled = false;
        } else {
        //   $(".error_email").prepend('<i class="fas fa-info-circle">');
          document.getElementById('uname_error_email').innerHTML = 'Error: Địa chỉ Email không đúng định dạng!';
          document.getElementById('save').disabled = true;
          document.getElementById('usave').disabled = true;
        }
    } else {
      document.getElementById('uname_error_email').innerHTML = 'Error: Hãy nhập địa chỉ Email!';
      document.getElementById('save').disabled = true;
      document.getElementById('usave').disabled = true;
    }
});
  
function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
    return pattern.test(emailAddress);
}

function removeAscent (str) {
    if (str === null || str === undefined) return str;
    str = str.toLowerCase();
    str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a");
    str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e");
    str = str.replace(/ì|í|ị|ỉ|ĩ/g, "i");
    str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o");
    str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u");
    str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y");
    str = str.replace(/đ/g, "d");
    return str;
}
function isValid_Unicode(string) {
    var charReg = /^[a-zA-Z\$%\^\&*\)\(+=._-]{2,}$/g // regex here
    return charReg.test(removeAscent(string))
}
var id_password1  = document.getElementById("id_password1"),
id_password2  = document.getElementById("id_password2");
uusermsg = document.getElementById("uname_error_ma");
function checkPassword(){
   
    var error = "";
    document.getElementById('uname_error_ma').innerHTML = '';
    document.getElementById('save').disabled = false;
    document.getElementById('usave').disabled = false;
    if(id_password1.value.length==0)
    {
        error = "Error: Hãy nhập mật khẩu!";
        document.getElementById('uname_error_ma').innerHTML = error;
        id_password1.focus();
        document.getElementById('save').disabled = true;
        document.getElementById('usave').disabled = true;
    } else if(id_password1.value.length != 0)
    {
        if(id_password1.value.length < 8) {
            error = "Error: Mật khẩu phải có ít nhất bao gồm 8 ký tự!";
            document.getElementById('uname_error_ma').innerHTML = error;
            id_password1.focus();
            document.getElementById('save').disabled = true;
            document.getElementById('usave').disabled = true;
        }
        re = /[0-9]/;
        if(!re.test(id_password1.value)) {
            error = "Error: Mật khẩu phải chứa ít nhất 1 chữ số (0-9)!";
            document.getElementById('uname_error_ma').innerHTML = error;
            id_password1.focus();
            document.getElementById('save').disabled = true;
            document.getElementById('usave').disabled = true;
        }
        re = /[a-z]/;
        if(!re.test(id_password1.value)) {
            error = "Error: Mật khẩu phải chứa ít nhất một chữ cái viết thường (a-z)!";
            document.getElementById('uname_error_ma').innerHTML = error;
            id_password1.focus();
            document.getElementById('save').disabled = true;
            document.getElementById('usave').disabled = true;
        }
        re = /[A-Z]/;
        if(!re.test(id_password1.value)) {
            error = "Error: Mật khẩu phải chứa ít nhất một chữ cái viết hoa (A-Z)!";
            document.getElementById('uname_error_ma').innerHTML = error;
            id_password1.focus();
            document.getElementById('save').disabled = true;
            document.getElementById('usave').disabled = true;
        }
        if(id_password2.value.length==0)
        {
            error = "Error: Hãy nhập mật khẩu để xác nhận!";
            document.getElementById('uname_error_ma').innerHTML = error;
            id_password2.focus();
            document.getElementById('save').disabled = true;
            document.getElementById('usave').disabled = true;
        } else if (id_password1.value != id_password2.value){
            document.getElementById('uname_error_ma').innerHTML = 'Error: Mật khẩu không khớp!';
            id_password2.focus();
            document.getElementById('save').disabled = true;
            document.getElementById('usave').disabled = true;
        }
    }
}

function CheckAllForm(flag) {
    if(flag!='EDIT_USER'){
        document.getElementById("uname_e_username").innerHTML = '';
        document.getElementById("uname_error_ma").innerHTML = '';
    }
    document.getElementById("uname_error_msg").innerHTML = '';
    document.getElementById("uname_error_email").innerHTML = '';
    var id_ma_cay = document.getElementById('id_ma_cay').value;
    if (id_ma_cay.length == 0){
        document.getElementById("uname_e_username").innerHTML = 'Error: Hãy nhập Username!';
        document.getElementById('id_ma_cay').focus();
        return false;
    }
    else{ 
        var charReg = /^\s*[a-zA-Z0-9,\s]+\s*$/;
        if (!charReg.test(id_ma_cay)) {
            document.getElementById("uname_e_username").innerHTML = 'Error: Username không chấp nhập các chữ số đặt biệt!';
            document.getElementById('id_ma_cay').focus();
            return false;
        }
    }
    if (flag!='EDIT_USER'){
        if (document.getElementById('id_password1').value.length == 0){
            document.getElementById("uname_error_ma").innerHTML = 'Error: Hãy nhập mật khẩu!';
            document.getElementById('id_password1').focus();
            return false;
        }
        var lengthPass = document.getElementById('id_password1').value.length;
        if (!(lengthPass > 8 || lengthPass < 20)) {
            document.getElementById("uname_error_ma").innerHTML = 'Error: Độ dài mật khẩu phải lớn hơn hoặc bằng 8 ký tự trở lên!';
            document.getElementById("uname_error_ma").focus();
            return false
        }
        if (document.getElementById('id_password2').value.length == 0){
            document.getElementById("uname_error_ma").innerHTML = 'Error: Hãy nhập mật khẩu!';
            document.getElementById("id_password2").focus();
            return false;
        }
        if(document.getElementById('id_password1').value.length != 0 && document.getElementById('id_password1').value == document.getElementById('id_password2').value) {
            if(!checkvalidPassword(document.getElementById('id_password1').value)) {
                document.getElementById("uname_error_ma").innerHTML = 'Error: Mật khẩu phải bao gồm ít nhất 8 ký tự (bao gồm: chữ hoa, chữ thường và số)!';
                document.getElementById("id_password2").focus();
                return false;
            }
        }
        if(document.getElementById('id_password1').value != document.getElementById('id_password2').value){
            document.getElementById("uname_error_ma").innerHTML = 'Error: Mật khẩu không khớp!';
            document.getElementById("id_password2").focus();
            return false;
        }
    }
    if (document.getElementById('id_first_name').value.length == 0){
         document.getElementById("uname_error_msg").innerHTML = 'Error: Hãy nhập họ tên!';
        document.getElementById("id_first_name").focus();
        return false;
    }
    if (document.getElementById('id_last_name').value.length == 0){
        document.getElementById("uname_error_msg").innerHTML = 'Error: Hãy nhập họ tên!';
        document.getElementById("id_last_name").focus();
        return false;
    }
    //var format = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
    var inputFullnameVal = removeAscent(document.getElementById('id_first_name').value + " " + document.getElementById('id_last_name').value);
    if(/[0-9]/.test(inputFullnameVal)){
        document.getElementById("uname_error_msg").innerHTML = 'Error: Họ tên không chấp nhập chữ số!';
        document.getElementById("id_first_name").focus();
        return false;
    }
    if (format.test(inputFullnameVal)){
        document.getElementById("uname_error_msg").innerHTML = 'Error: Họ tên không chấp nhập các chữ số đặt biệt!';
        document.getElementById("id_first_name").focus();
        return false;
    }
    if (document.getElementById('id_email').value.length == 0){
        document.getElementById("uname_error_email").innerHTML = 'Error: Hãy nhập địa chỉ email!';
        document.getElementById("id_email").focus();
        return false;
    }else{
        var check = false;
        var valueMail = document.getElementById("id_email").value;
        var shtrudel = 0;
        for (var i = 0; i < valueMail.length; i++) {
            if (valueMail.charAt(i) == '@') {
                shtrudel++;
                for (var j = i; j < valueMail.length; j++) {
                if (valueMail.charAt(j) == '.') {
                    check = true;
                    }
                }
            }
        }
        if (shtrudel > 1) {
            document.getElementById('uname_error_email').innerHTML = "Error: Địa chỉ Email chỉ được phép có 1 dấu '@'!";
            document.getElementById("id_email").focus();
            return false;
        }
        if (!check) {
            document.getElementById('uname_error_email').innerHTML = "Error: Địa chỉ Email của bạn phải bao gồm dấu '@' và '.'!";
            document.getElementById("id_email").focus();
            return false;
        }
        if(!isValidEmailAddress(document.getElementById('id_email').value))
        {
            document.getElementById('uname_error_email').innerHTML = 'Error: Địa chỉ Email không đúng định dạng!';
            document.getElementById("id_email").focus();
            return false;
        }
    }
    return true;
}