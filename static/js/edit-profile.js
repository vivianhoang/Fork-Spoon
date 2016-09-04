var maxLength = 1000;

$('textarea').keyup(function() {
    var length = $(this).val().length;
    var new_length = maxLength-length;
    $('#chars').text(new_length);
});

function showConfirmation(result) {
    alert(result);
}

function updateProfile(evt) {
    evt.preventDefault();

    // can't use .val() because textarea doesn't have that attribute
    var formInputs = {
        "description": $(".profile-bio").val()
    };

    console.log(formInputs);

    $.post("/profile-edit",
        formInputs,
        showConfirmation
        );
}

$("#profile-description").on("submit", updateProfile);