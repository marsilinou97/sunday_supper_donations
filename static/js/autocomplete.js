function onAutocompleteItemSelect(event, ui) {
    $("#id_first_name").val(ui.item.first_name);
    $("#id_last_name").val(ui.item.last_name);
    $("#id_email").val(ui.item.email_address);
    $("#id_phone_number").val(ui.item.phone_number);
    $("#id_address1").val(ui.item.address_line1);
    $("#id_address2").val(ui.item.address_line2);
    $("#id_city").val(ui.item.city);
    $("#id_state").val(ui.item.state); // might not be that easy but let's find out :)
    $("#id_zip").val(ui.item.zipcode);
    // // debug
    // console.log(ui.item.first_name + " " + ui.item.email + " " + ui.item.phone_number + " " + ui.item.address1 + " " + ui.item.address2 + " " + ui.item.city + " " + ui.item.state + " " + ui.item.zipcode);
    return false;
}

function prettyPrintAutocompleteResults(autocompleteFunction) {
    autocompleteFunction.autocomplete("instance")._renderItem = function (ul, item) {
        // build the li option for the ul element
        // the donor always has at least a first name
        // the user won't be able to see " " + "" so we don't have to worry about the last name being blank
        var option = "<div><strong>" + item.first_name + " " + item.last_name + "</strong>";

        // add the email, phone, address lines (if they exist)
        if (!(item.email_address === "")) {
            option = option + "<br>" + item.email_address;
        }
        if (!(item.phone_number === "")) {
            option = option + "<br>" + item.phone_number;
        }
        if (!(item.address_line1 === "")) {
            option = option + "<br>" + item.address_line1;
        }
        if (!(item.address_line2 === "")) {
            option = option + "<br>" + item.address_line2;
        }

        // if the city, state, or zipcode exist, add them in "city, state, zipcode" format
        // any blank attributes here get filled with ?'s
        if (!(item.city === "" && item.state === "" && item.zipcode === "")) {
            option = option + "<br>";
            if (item.city === "") {
                option = option + "?, ";
            } else {
                option = option + item.city + ", ";
            }
            if (item.state === "") {
                option = option + "?, ";
            } else {
                option = option + item.state + ", ";
            }
            if (item.zipcode === "") {
                option = option + "?";
            } else {
                option = option + item.zipcode;
            }
        }
        option = option + "</div>";

        return $("<li>").append(option).appendTo(ul);
    };
}

$(function () {
    // autocomplete 'em
    prettyPrintAutocompleteResults($('#id_first_name').autocomplete({
        minLength: 2,
        source: "get_donors/?name_type=first",
        focus: function (event, ui) {
            $("#id_first_name").val(ui.item.first_name);
            return false;
        },
        select: onAutocompleteItemSelect,
        messages: {
            noResults: function (_) {
                console.log("There were no matches.")
                // $('#id_first_name').autocomplete("disable");
            },
            results: function (count) {
                console.log("There were " + count + " matches")
            }
        }
    }));

    prettyPrintAutocompleteResults($('#id_last_name').autocomplete({
        minLength: 2,
        source: "get_donors/?name_type=last",
        focus: function (event, ui) {
            $("#id_last_name").val(ui.item.last_name);
            return false;
        },
        select: onAutocompleteItemSelect
    }))
});


/* Disable browser autocomplete, we can enable that only when the autocomplete functionality is enabled */
$("input").focus(function () {
    $(this).attr("autocomplete", "new-password")
});

$('input').blur(function () {
    $(this).removeAttr('autocomplete');
});