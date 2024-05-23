function getFormDataAsUrlEncoded(form) {
    var formData = new FormData(form);
    var params = new URLSearchParams();
    for (var pair of formData.entries()) {
        params.append(pair[0], pair[1]);
    }
    return params.toString();
}


function signin() {
    var form = $('#UserLoginForm')[0]; // Obtén el elemento DOM
    var formData = getFormDataAsUrlEncoded(form);

    $.ajax({
        type: "POST",
        url: "/auth/token",
        data: formData,
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        processData: false,
        headers: {
            "Accept": "application/json"
        }
    }).done(function(data) {
        console.log(data);
    }).fail(function(jqXHR) {
        console.error('Error:', jqXHR.status, jqXHR.statusText);
        alert('An error occurred when submitting to sign-in URL! Please try again later.');
    });
}

function signup() {
    alert("SIGNING-UP!");
}