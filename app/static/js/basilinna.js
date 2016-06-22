
// 组件显示隐藏
function showItem(id) {
    var item = document.getElementById(id);
    item.style.display = "block";
}
function hiddenItem(id) {
    var item = document.getElementById(id);
    item.style.display = "none";
}

// 修改属性
function setMsg(id, msg) {
    var item = document.getElementById(id);
    item.innerHTML = msg;
}

// 校验
function validate(func, error_alert, sid, error_msg) {
    if(func) {
        hiddenItem(error_alert);
        // setMsg(sid, "form-group has-success");
    }else {
        showItem(error_alert);
        setMsg(sid, error_msg);
    }
}

// 校验邮箱
function check_email(id) {
    var email = document.getElementById(id).value.trim();
    var reg = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    if (!reg.test(email)) {
        return false;
    } else {
        return true;
    }
}

// 校验昵称
function check_name(id) {
    var nickname = document.getElementById(id).value.trim();
    var reg = /^.{2,20}$/;
    if (!reg.test(nickname)) {
        return false;
    } else {
        return true;
    }
}

// 校验密码
function check_pass(id) {
    var password = document.getElementById(id).value.trim();
    var reg = /^[a-zA-Z_][a-zA-Z0-9_]{5,127}$/;
    if (!reg.test(password)) {
        return false;
    } else {
        return true;
    }
}

// 校验密码一致性
function check_confirmPass(id, cid) {
    var password = document.getElementById(id).value.trim();
    var confirmPassword = document.getElementById(cid).value.trim();
    if ((password == "") | (confirmPassword == "")
            | (password != confirmPassword)) {
        return false;
    } else {
        return true;
    }
}

// 同意条款
function check_terms(id) {
    var terms = document.getElementById(id);
    return terms.checked;
}