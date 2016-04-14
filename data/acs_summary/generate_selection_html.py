import json

with open("acs_summary/variables.json") as f:
    data = json.load(f)

html_file = open("acs_summary/select.html", "w")

def emit(s):
    html_file.write(s)

def emitLine(line):
    emit(line + "\n")

def emitMulti(*args):
    emit(" ".join(args))

def emitMultiWithLine(*args):
    emitLine(" ".join(args))

def emitStartTag(tag, attributes={}):
    args = ["<" + tag]
    args += [("%s='%s'" % t) for t in attributes.items()]
    args.append(">")
    emitMultiWithLine(*args)

def emitEndTag(tag):
    emitLine("</" + tag + ">")

def emitTag(tag, attributes={}, content=""):
    args = ["<" + tag]
    args += [("%s='%s'" % t) for t in attributes.items()]
    args.append(">" + content + "</" + tag + ">")
    emitMultiWithLine(*args)

def renderHeader():
    emit("""
<html>
<head>
<style>
div, body, html {
    margin: 0px;
    padding: 0px;
}

.topic-header {
    display: inline-block;
}
.topic {
    padding: 10px;
}
.topic:nth-child(even) {
    background-color: #ddddff;
}
.topic:nth-child(odd) {
    background-color: #ccccff;
}
.topic-children {
    margin-left: 2em;
}

.group {
    padding: 10px;
}
.group:nth-child(even) {
    background-color: #eeffee;
}
.group:nth-child(odd) {
    background-color: #ffffff;
}
.group-children {
    margin-left: 2em;
}

.table:nth-child(even) {
    background-color: #eeeeee;
}
.table:nth-child(odd) {
    background-color: #dddddd;
}
.table-children {
    display: none;
    margin-left: 2em;
}
.partial-check {
    opacity: 0.5;
}

.variable {
}
.variable:nth-child(even) {
    background-color: #f8f8f8;
}
.variable:nth-child(odd) {
    background-color: #ffffff;
}

.restriction {
    color: red;
}

/* Tooltip container */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltip-text {
    visibility: hidden;
    width: 120px;
    background-color: black;
    color: #fff;
    text-align: center;
    padding: 5px 0;
    border-radius: 6px;

    /* Position the tooltip text - see examples below! */
    position: absolute;
    z-index: 1;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltip-text {
    visibility: visible;
}

.set-children {
    display: none;
}

</style>
<script src='https://code.jquery.com/jquery-2.2.3.min.js' type='text/javascript'>
</script>
<script>
var toggleVisibility = function (e) {
    if (e.css('display') == 'block') {
        e.css('display', 'none');
    } else {
        e.css('display', 'block');
    }
};

var toggleCollapse = function(ev) {
    elem = $(this);
    thisClass = elem.attr('class').split(/\s+/)[0];
    baseClass = thisClass.split('-')[0];
    if (baseClass != thisClass) {
        elem = elem.parents('.' + baseClass);
    }
    childClass = baseClass + "-children";
    child = elem.find("." + childClass);
    toggleVisibility(child);
    ev.stopPropagation();
    return false;
};

var getTableState = function(table) {
    variables = table.find('.variable-select');
    foundChecked = false;
    foundUnchecked = false;
    variables.each( function(i, elem) {
        if ($(elem).prop('checked')) {
            foundChecked = true;
        } else {
            foundUnchecked = true;
        }
    });
    if (foundChecked && foundUnchecked) {
        return 'partial';
    } else if (foundChecked) {
        return 'all';
    } else {
        return 'none';
    }
};

var setVariablesChecked = function(table, checked) {
    variables = table.find('.variable-select');
    variables.prop('checked', checked);
};

var setTableState = function(table, state) {
    checkbox = table.find('.table-select');
    if (state == 'all') {
        checkbox.prop('checked', true);
        checkbox.removeClass('partial-check');
    } else if (state == 'partial') {
        checkbox.prop('checked', true);
        checkbox.addClass('partial-check');
    } else if (state == 'none') {
        checkbox.prop('checked', false);
        checkbox.removeClass('partial-check');
    }
};

var toggleTable = function(ev) {
    elem = $(this);
    table = elem.parent().parent();
    elem.prop('checked', true);
    var tableState = getTableState(table);
    if (tableState != 'all') {
        setVariablesChecked(table, true);
        setTableState(table, 'all');
    } else {
        setVariablesChecked(table, false);
        setTableState(table, 'none');
    }
    ev.stopPropagation();
};

var toggleVariable = function(ev) {
    elem = $(this).parents('.variable');
    var cb = elem.find('.variable-select');
    cb.prop('checked', ! cb.prop('checked'));
    ev.stopPropagation();
    variableWasToggled(elem);
}

var clickedVariable = function(ev) {
    elem = $(this).parents('.variable');
    ev.stopPropagation();
    variableWasToggled(elem);
};

var variableWasToggled = function(variable) {
    var table = variable.parents('.table');
    setTableState(table, getTableState(table));
};

var getSelections = function() {
    var variables = $('.variable')
    selectedIds = ''
    variables.each(function(i, e) {
        variable = $(e);
        var selected = variable.find('.variable-select').prop('checked');
        if (selected) {
            selectedIds += variable.attr('id') + '\\n';
        }
    })
    console.log(selectedIds);
    var blob = new Blob([selectedIds], {type : 'text/plain'});
    var url = URL.createObjectURL(blob);
    window.open(url);
}

var getSelections = function() {
    var variables = $('.variable')
    selectedIds = ''
    variables.each(function(i, e) {
        variable = $(e);
        var selected = variable.find('.variable-select').prop('checked');
        if (selected) {
            selectedIds += variable.attr('id') + '\\n';
        }
    })
    console.log(selectedIds);
    var blob = new Blob([selectedIds], {type : 'text/plain'});
    var url = URL.createObjectURL(blob);
    window.open(url);
}

var setSelections = function() {
    var text = $('#set-text').val();
    $('.variable-select').prop('checked', false);
    text.split('\\n').forEach(function(varId) {
        if (varId == '') {
            return;
        }
        var variable = $('#' + varId);
        var cb = $('#select-' + varId);
        cb.prop('checked', true);
        console.log($('#' + varId + ' .variable-select'))
    })
    $('.table').each(function(i, e) {
        var table = $(e);
        setTableState(table, getTableState(table));
    })
    console.log(text);
}

$(function() {
    $('.table-description').on('click', toggleCollapse);
    $('.set-header').on('click', toggleCollapse);
    $('.group').on('click', toggleCollapse);
    $('.topic-description').on('click', toggleCollapse);
    $('.table-select').on('click', toggleTable);
    $('.variable-select').on('click', clickedVariable);
    $('.variable-description').on('click', toggleVariable);
    $('#get').on('click', getSelections);
    $('#set-submit').on('click', setSelections);

})
</script>
</head>
<body>
<h1>ACS Variables and Tables</h1>
<h2><a id='get' href='#'>Get selections</a></h2>
<div class='set'>
<h2 class='set-header'>Set selections</h2>
<div class='set-children'>
<textarea name="set" id='set-text' cols="30" rows="15" ></textarea>
<button id='set-submit'>Go</button>
</div>

</div>


""")

def renderFooter():
    emit("""
</body>
</html>
""")

def renderTopicStart(topic):
    emitStartTag(
        "div",
        {
            "class": "topic",
            "id": topic["id"]
        }
    )
    group = data["groups"][topic["groups"][0]]
    table = data["tables"][group["tables"][0]]
    topicSummary = table["description"]
    emitStartTag("div", {"class": "topic-description"})
    emitTag("h3", {
        "class": "topic-header"
    }, topic["id"])
    emitTag("span", content=topicSummary)
    emitEndTag("div")
    emitStartTag(
        "div",
        {
            "class": "topic-children",
            "id": topic["id"]
        }
    )
    pass

def renderTopicEnd(topic):
    emitEndTag("div")
    emitEndTag("div")
    pass


def renderGroupStart(group, topic):
    if len(group["tables"]) > 1:
        emitStartTag(
            "div",
            {
                "class": "group group-multi",
                "id": group["id"]
            }
        )
        table = data["tables"][group["tables"][0]]
        emitTag("h4", {
            "class": "group-header"
        }, group["id"] + " - " + table["description"])
        emitStartTag(
            "div",
            {
                "class": "group-children",
                "id": group["id"]
            }
        )
    else:
        return

def renderGroupEnd(group, topic):
    if len(group["tables"]) > 1:
        emitEndTag("div")
        emitEndTag("div")
    pass


restrictionsCodes = {
    "US Only": "US",
    "Migration PR Only": "MPR",
    "Migration US Only": "MUS",
    "Nation and State Only": "NS",
    "No Blockgroups": "BG",
    "Place of Work Only": "PW",
    "Nation, States, and Counties Only": "NSC",
    "PR Only": "PR",
    "Nation and States Only (Excluding PR)": "NS",
    "Nation Only": "NAT"
}

def renderTableStart(table, group, topic):
    emitStartTag(
        "div",
        {
            "class": "table",
            "id": table["id"]
        }
    )
    emitStartTag(
        "div",
        {"class": "table-description"}
    )
    tableDescription = " - ".join([
        table["id"],
        str(table["size"]),
        table["description"]
    ])
    emitTag(
        "input",
        {
            "type": "checkbox",
            "class": "table-select",
            "id": "select-" + table["id"]
        }
    )
    emitTag(
        "span",
        {"class": "table-title"},
        tableDescription
    )
    if table["restrictions"] is not None:
        restrictionsCode = restrictionsCodes[table["restrictions"]]
        emitStartTag(
            "span",
            {"class": "restriction tooltip"}
        )
        emitLine(restrictionsCode)
        emitTag(
            "span",
            {"class": "tooltip-text"},
            table["restrictions"]
        )
        emitEndTag("span")
    emitEndTag('div')
    emitStartTag(
        "div",
        {"class": "table-children"}
    )
    pass

def renderTableEnd(table, group, topic):
    emitEndTag("div")
    emitEndTag("div")
    pass

def renderVariable(variable, table, group, topic):
    emitStartTag(
        "div",
        {
            "class": "variable",
            "id": variable["id"]
        }
    )
    emitTag(
        "input",
        {
            "type": "checkbox",
            "class": "variable-select",
            "id": "select-" + variable["id"]
        }
    )
    emitTag(
        "span",
        {"class": "variable-description"},
        variable["description"]
    )
    emitEndTag("div")

renderHeader()

allRestrictions = set()

for topicId in data["topicIds"]:
    topic = data["topics"][topicId]
    renderTopicStart(topic)
    for groupId in topic["groups"]:
        group = data["groups"][groupId]
        renderGroupStart(group, topic)
        for tableId in group["tables"]:
            table = data["tables"][tableId]
            renderTableStart(table, group, topic)
            for varId in table["variables"]:
                variable = data["variables"][varId]
                renderVariable(variable, table, group, topic)
            renderTableEnd(table, group, topic)
        renderGroupEnd(group, topic)
    renderTopicEnd(topic)

renderFooter()
