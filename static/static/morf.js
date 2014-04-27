var typewatch = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  }
})();


function load_model_box() {

    $.getJSON('models', function(resp) {
        console.log(resp);
        var $tbody = $("#langtable").find("tbody");
        $tbody.empty();

        $.each(resp.models, function(idx, model) {
            $tbody.append($("<tr>").append(
                $("<td>").text(model[0]),
                $("<td>").append(
                    $("<input>").attr({
                        id: 'model-'+idx,
                        type: 'radio',
                        name: 'model',
                        value: model[1],
                        checked: idx==0
                    }).change(select_model),
                    $("<label>").attr({
                        id: 'lbl-model-'+idx,
                        for: 'model-'+idx
                    }).text(model[2])
                )
            ));
        });
        select_model();
    });
}

function select_model() {
    "use strict";
    var model = $('input[name=model]:checked').val()
    console.log(model + " selected");

    $('#word').val("");

    $.getJSON('info/'+model, function(resp) {
        console.log(resp);
        var $infobox = $("#infobox");
        $infobox.empty();

        var $list = $("<dl>");

        $list.append($("<dt>").text("Num word forms"))
            .append($("<dd>").text(resp.num_compounds));

        $list.append($("<dt>").text("Num morph types"))
            .append($("<dd>").text(resp.num_morphs));

        $list.append($("<dt>").text("Corpusweight"))
            .append($("<dd>").text(resp.corpus_weight.toFixed(2)));

        $infobox.append($("<div>").addClass("subinfo").append($list));

        if (resp.supervised) {
            $list = $("<dl>");

            $list.append($("<dt>").text("Num annotations"))
            .append($("<dd>").text(resp.num_annotations));

            $list.append($("<dt>").text("Annotationweight"))
            .append($("<dd>").text(resp.annotation_weight.toFixed(2)));

            $infobox.append($("<div>").addClass("subinfo").append($list));
        }

        var $special_chars = $("#special_chars");
        $special_chars.empty();

        var $inputbox = $('#word');
        $.each(resp.special_chars, function(idx, char) {
            $special_chars.append($("<button>").text(char).on('click', function() {
                $inputbox.focus();
                var orig_word = $inputbox.val();
                $inputbox.val(orig_word + char);
                do_segmentation();
            }));
        });

        if (resp.hasOwnProperty('evalwords')) {
            var $button = $("#randword");
            $button.show();
            $button.on('click', function () {
                $("#word").val(resp.evalwords[Math.floor(Math.random()*resp.evalwords.length)])
                do_segmentation();
            })
        } else {
            $("#randword").hide();
        }
    });

    clear_results();

}

function clear_results() {
    "use strict";
    $("#resultcorrect").hide();
    $("#result1").find("table").empty();
    $("#result2").hide().find("table").empty();
    $("#word").focus();

}

function make_result_table(table, results) {
//    var total_weight_sum =
    //<tr><td><span style='font-size:3.26em'>kansanedustaja</span></td><td>11.8<td></tr>
    var total_font_size = 10;

    table.empty();
    $.each(results, function (idx, result) {
        table.append(
            $("<tr>").append(
                $("<td>").append(
                    $("<span>")
                        .text(result.segm.join(" + "))
                        .css('font-size', (result.fsize * total_font_size) + 'em')
                        .css('color', result.correct ? 'green' : 'black')
                ),
                $("<td>").text(result.cost.toFixed(1))
            ))
    })
}

function do_segmentation() {
    clear_results();
    var model = $('input[name=model]:checked').val();
    var word = $('#word').val().toLowerCase();
    fetch_segmentation(model, word);
}

function fetch_segmentation(model, word) {
    var $result1_table = $("#result1").find("table");
    var $result2_table = $("#result2").find("table");

//    $result1_table.empty();
//    $result2_table.empty();

    if (word.length == 0) return;

    $.getJSON('segment/'+encodeURIComponent(model)+'/'+encodeURIComponent(word), function(resp) {
        console.log(resp);

        make_result_table($result1_table, resp.standard);

        if("anno" in resp) {
            $("#result2").show();
            make_result_table($result2_table, resp.anno);
        }

        if("correct" in resp) {
            $result_correct = $("#resultcorrect");
            $result_correct.show();
            var $correct_table = $result_correct.find("table");
            $correct_table.empty();
            $.each(resp.correct, function (idx, result) {
                $correct_table.append(
                    $("<tr>").append(
                        $("<td>").append(
                            $("<span>")
                                .text(result.join(" + "))

                        )
                    ))
    })
        }

    });
}
