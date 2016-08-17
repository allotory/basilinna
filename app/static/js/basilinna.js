
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
        return true;
    }else {
        showItem(error_alert);
        setMsg(sid, error_msg);
        return false;
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

// 提交校验
function validateSubmit() {
    var isEmailChecked = validate(check_email("email"), "validate_error", "error_msg", "邮件地址不正确");
    var isNicknameChecked = validate(check_name('nickname'), 'validate_error', 'error_msg', '昵称长度应大于2个字符，小于20个字符');
    var isPasswordChecked = validate(check_pass('password'), 'validate_error', 'error_msg', '请输入6-128位，以字母及_开头的密码');
    var isConfirmPassChecked = validate(check_confirmPass('password', 'confirm_password'), 'validate_error', 'error_msg', '两次密码输入不一致');
    var isTermsChecked = validate(check_terms('terms'), 'validate_error', 'error_msg', '需同意隐私协议及服务条款');
    
    if(!(isNicknameChecked && isEmailChecked && isPasswordChecked 
        && isConfirmPassChecked && isTermsChecked)) {
        return false;
    }
    return true;
}

// 登陆提交校验
function validateLogin() {
    var isEmailChecked = validate(check_email('email'), 'validate_error', 'error_msg', '邮件地址不正确');
    var isPasswordChecked = validate(check_pass('password'), 'validate_error', 'error_msg', '请输入6-128位，以字母及_开头的密码');
    if(!(isEmailChecked && isPasswordChecked)) {
        return false;
    }
    return true;
}

// 校验设置用户昵称
function check_fullname(id, name) {

    var fullname = document.getElementById(id).value.trim();

    if(fullname == '') {
        fullname = name;
    }
    // alert(obj.value);
    var name_len = fullname.length;
    if((name_len >= 4) && (name_len <= 12)) {
        return true;
    }
    return false;
}

// 校验个性域名
function check_purl(id, purl) {

    var personal_url = document.getElementById(id).value.trim();

    if (personal_url == '') {
        personal_url = purl;
    }
    var reg = /^[a-zA-Z_][a-zA-Z0-9_]{5,19}$/;
    if (!reg.test(personal_url)) {
        return false;
    } else {
        return true;
    }
}

// 校验年份
function check_year(id) {
    var year = document.getElementById(id).value.trim();

    if (year == '') {
        year = 0;
        return true;
    } else {

        y = parseInt(year)

        if (y >= 1900 && y <= 2016) {
            return true;
        } else {
            return false;
        }
    }
}

// 个人信息提交校验
function validateInfo(fullname, purl) {

    var a = document.getElementById("month").value.trim();

    alert(a);

    return false;

    // var isFullnameChecked = validate(check_fullname('fullname', fullname), 'validate_error', 'error_msg', '不超过 4 - 12 个字符，请勿使用特殊字符');
    // var isPersonalUrl = validate(check_purl('personality_url', purl), 'validate_error', 'error_msg', '不超过 6 - 20 个字符，请勿使用特殊字符');
    // if(!(isFullnameChecked && isPersonalUrl)) {
    //     return false;
    // }
    // return true;
}