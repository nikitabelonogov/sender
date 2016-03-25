function userlink(user) {
    var span = document.createElement('span');
    span.setAttribute('class', 'userlink');
    var a = document.createElement('a');
    a.setAttribute('href', '/user/'+user.id);
    a.innerHTML = twemoji.parse(String.fromCodePoint(user.emoji))+user.username;
    span.appendChild(a);
    return span;
}
function printmessage(data){
    var div = document.createElement('div');
    div.setAttribute('class', 'message');
    div.appendChild(userlink(data.sender));
    div.innerHTML += ' : ';
    var time = document.createElement('span');
    time.setAttribute('class', 'timestamp');
    time.innerHTML = data.timestamp;
    div.appendChild(time);
    var text = document.createElement('div');
    text.setAttribute('class', 'messagetext');
    text.innerHTML = twemoji.parse(data.text);
    div.appendChild(text);
    return div;
}
function printdialog(dialog){
    var div = document.createElement('div');
    div.appendChild(userlink(dialog.user1))
    div.innerHTML += " & ";
    div.appendChild(userlink(dialog.user2))
    div.innerHTML += " : ";
    return div;
}