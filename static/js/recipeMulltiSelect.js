function applyEventListenerToAllSelect(){
    $(".select.custom-select.timeSelector").mousedown(function (e) {
        mouseDownOnSelect(e, this);
    })
    .mousemove(function (e) {
        mouseMoveOnSelect(e, this);
    });
}

  function applyEventListenerToSpecificSelect(element){
    var parentElement = element.closest('.select.custom-select.timeSelector');
    if ($._data(parentElement, "events").hasOwnProperty("mousedown")){
      if ($._data(parentElement, "events").mousedown.length > 0){
        return;
      }
    }

    $(parentElement).mousedown(function (e) {
        mouseDownOnSelect(e, this);
    })
    .mousemove(function (e) {
        mouseMoveOnSelect(e, this);
    });
}

function mouseDownOnSelect(e, element){
    e.preventDefault();

    let select = element;
    scroll = select.scrollTop;

    if(e.target.index == undefined){
        return;
    }

    if (!e.target.selected) {
        e.target.selected = true;
        select.options[e.target.index].selected = true;

    } else if (e.target.selected) {
        e.target.selected = false;
        select.options[e.target.index].selected = false;
    }

    setTimeout(function () {
        select.scrollTop = scroll;
    }, 0);

    $(select).focus();
}

function mouseMoveOnSelect(e, element){
    e.preventDefault();
}

function isMobile() {
    return window.innerWidth <= 768; // Adjust the threshold as needed
}