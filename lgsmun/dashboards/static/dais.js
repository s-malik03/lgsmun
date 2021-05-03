function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function set_zoom_link(){
  $.post("set_zoom_link",{
    'zoom_link':$('#zl').val(),
    'csrfmiddlewaretoken':csrftoken
  });
}
function set_drive_link(){
  $.post("set_drive_link",{
    'drive_link':$('#dl').val(),
    'csrfmiddlewaretoken':csrftoken
  });
}
function send_notification(){
  $.post("send_notification",{
    'notification':$('#noti').val(),
    'csrfmiddlewaretoken':csrftoken
  });
  $('#noti').val('');
}
function set_total_time(){
  var m=parseInt($('#t_min').val());
  var s=parseInt($('#t_sec').val());
  $('#total_minutes').html(m.toLocaleString(undefined, {minimumIntegerDigits: 2}));
  $('#total_seconds').html(s.toLocaleString(undefined, {minimumIntegerDigits: 2}));
  s=s+(m*60);
  $.post("set_total_time",{
    'duration':s.toString(),
    'csrfmiddlewaretoken':csrftoken
  });

}
var general_s=0;
function set_speaker_time(){
  var m=parseInt($('#min').val());
  var s=parseInt($('#sec').val());
  $('#minutes').html(m.toLocaleString(undefined, {minimumIntegerDigits: 2}));
  $('#seconds').html(s.toLocaleString(undefined, {minimumIntegerDigits: 2}));
  s=s+(m*60);
  general_s=s;
  $.post("set_speaker_time",{
    'duration':s.toString(),
    'csrfmiddlewaretoken':csrftoken
  });

}
function floor_mod(){
  $.post('add_mod',{
    'mod':$('#mod_val').val(),
    'csrfmiddlewaretoken':csrftoken
  });
  $('#mod_val').val('');
}
function remove_mod(){
  $.post('remove_mod',{
    'modnum':parseInt($('#modnum').val()),
    'csrfmiddlewaretoken':csrftoken
  });
  $('#modnum').val(0);
}
function set_mod(){
  $.post('set_current_mod',{
    'current_mod':$('#set_mod').val(),
    'csrfmiddlewaretoken':csrftoken
  });
  $('#set_mod').val('');
}
function set_topic(){
  $.post('set_current_topic',{
    'topic':$('#set_topic').val(),
    'csrfmiddlewaretoken':csrftoken});
  $('#set_topic').val('');
}
function set_speaking_mode(){
  $.post('speaking_mode',{
    'speaking_mode':$('#set_speaking_mode').val(),
    'csrfmiddlewaretoken':csrftoken
  });
}
function add_speaker(){
  if(($('#speaking_mode').text()=='Idle')||($('#speaking_mode').text()=='UnMod')){
    alert('Speaking mode is set to Idle/UnMod! Please change to RSL or GSL to proceed further.');
  }
  else{
  $.post('add_speaker',{
    'country':$('#speaker').val(),
    'csrfmiddlewaretoken':csrftoken
  });}
}
function sendmessage(){
  $.post("send_message",{
    'message':$('#message').val(),
    'recipient':$('#recipient').val(),
    'csrfmiddlewaretoken':csrftoken
  });
  $('#message').val('');
}
function raise_point(){
  $.post("raise_motion",{
    'motion':$('#point').val(),
    'csrfmiddlewaretoken':csrftoken
  });
}
var duration=0;
var counter=0;
var total_time=0;
var total_count=0;
var status='';
function timer(){

  if((status!='pause') && (status!='stop')){

    $('#minutes').html(Math.trunc(counter/60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#seconds').html((counter%60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#total_minutes').html(Math.trunc(total_count/60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#total_seconds').html((total_count%60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    if (counter!=0){
    counter=counter-1;
    if ((total_count!=0 && status=='start')){

      total_count=total_count-1;

    }
}
}
}
var ws= new WebSocket("ws://"+window.location.host+'/ws/dais/');
var z=0;
var ess_data={'committee':$('#committee_name').html(),'country':$('#country').val(),'uuid':$('#uuid').val(), 'iteration':0};
ws.onopen=function(){
  ess_data={'committee':$('#committee_name').html(),'country':$('#country').val(),'uuid':$('#uuid').val(), 'iteration':0};
  console.log(ess_data);
ws.send(JSON.stringify(ess_data));
};

ws.onmessage=async function(event){
  if(event.data!="NULL"){
  var data=JSON.parse(event.data);
  console.log(data);
  $('#att').html(data.countrylist);
  $('#current_mod').html(data.current_mod);
  $('#current_topic').html(data.current_topic);
  $('#speaking_mode').html(data.speaking_mode);
  $('#notifications').html(data.notifications);
  $('#gsl').html(data.gsl);
  $('#rsl').html(data.rsl);
  $('#inbox').html(data.inbox);
  $('#mod_table').html(data.mods);
  ess_data['iteration']=data.iteration;
  status=data.timer_status;
  if(parseInt(data.total_time)!=total_time){
    total_time=parseInt(data.total_time);
    total_count=total_time;
  }
  if ('start'==data.timer_status && duration!=parseInt(data.timer_duration)){
    status=data.timer_status;
      duration=parseInt(data.timer_duration);
      counter=duration;
  }
  else if(data.timer_status=='stop'){
    status=data.timer_status;
    duration=general_s;
    counter=general_s;
  }
  }
  await sleep(1000);
  ws.send(JSON.stringify(ess_data));
  console.log(ess_data);
};
setInterval(function(){ws.send(JSON.stringify(ess_data));},1000);
setInterval(timer,1000);
