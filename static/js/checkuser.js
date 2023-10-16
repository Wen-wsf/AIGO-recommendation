// 檢查使用者名稱和密碼是否正確
function checkUser() {
    var result = document.getElementById("loginname").value;
    var password = document.getElementById("loginpwd").value;
    if (result != "root" || password != "123456") {
        window.alert("使用者名稱或密碼不正確：內建使用者名稱root，密碼123456");
        return false;
    } else {
        return true;
    }
};