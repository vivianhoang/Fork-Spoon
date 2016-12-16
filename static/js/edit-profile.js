var maxLength = 1000;

$('textarea1').keyup(function() {
    var length = $(this).val().length;
    var new_length = maxLength-length;
    $('.chars').text(new_length);
});

$('textarea2').keyup(function() {
    var length = $(this).val().length;
    var new_length = maxLength-length;
    $('.chars').text(new_length);
});

function showConfirmation(result) {
    alert(result);
}

function updateProfile(evt) {
    evt.preventDefault();

    // can't use .val() because textarea doesn't have that attribute
    var formInputs = {
        "category_id": $(".category").val()
        "company": $(".company-name").val()
        "description": $(".profile-bio").val()
        "prev-experience": $(".past-job").val()
        "city": $(".city").val()
        "url": $(".url").val()
    };

    console.log(formInputs);

    $.post("/profile-edit",
        formInputs,
        showConfirmation
        );
}

$("#profile-description").on("submit", updateProfile);