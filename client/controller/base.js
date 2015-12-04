$(document).ready(function()
{
  //vérification de la registration
  if(localStorage.getItem("user_id") == undefined)
  {
    $.get(SERVER+"/register", null, function(data)
    {
      if(data.state == "ok")
      {
        localStorage.setItem("user_id", data.id);
        console.log("register");
        updatePosition(data.id);
      }
    })
  }
  else
  {
      console.log("logged "+localStorage.getItem("user_id"));
    updatePosition(localStorage.getItem("user_id"));
  }
});

function updatePosition(id)
{
  navigator.geolocation.getCurrentPosition(function(position) {
    $.get(SERVER+"/update/"+id+"/"+position.coords.latitude+"/"+position.coords.longitude, null, function(data)
    {
      if(data.state == "ok")
      {
          console.log("position ok");
        checkDanger(id);
      }
    });
  });
}



function checkDanger(id)
{
  $.get(SERVER+"/danger/"+id, null, function(data)
  {
    if(data.state == "ok")
    {
      if(data.events.length == 0)
      {
        $("#usage").css("display", "block");
      }
      else
      {
        $("#center").css("display", "block");
        $("#event_name").html(data.events[0][2]);
        localStorage.setItem("event_id",data.events[0][0] );
        setCallbacksTVB();
      }
    }
  });
}

function setCallbacksTVB()
{
  $("#event_yes").click(function()
  {
    $.get(SERVER+"/read/"+localStorage.getItem("user_id")+"/"+localStorage.getItem("event_id"), null, function()
    {
      $("#hero").css("display", "none");
    });
  });
  $("#event_no").click(function()
  {
    $.get(SERVER+"/read/"+localStorage.getItem("user_id")+"/"+localStorage.getItem("event_id"), null, function()
    {
      $("#event_no").css("display", "none");
      $("#event_input").css("display", "inline-block");
      $("#event_input input[type=button]").click(function()
      {
          var value;
          if($("#event_input input[type=checkbox]").first().prop("checked") == true)
            value = "danger";
          else if($($("#event_input input[type=checkbox]")[1]).prop("checked") == true)
            value="wounded"
          if(value != undefined)
          {
            $.get(SERVER+"/response/"+localStorage.getItem("user_id")+"/"+value, null, function()
            {
              $("#hero").css("display", "none");

            });
          }
          else
            $("#hero").css("display", "none");

      });
    });

  });

}
