//题目个数
var question_num = 1;

//得分点个数
var point_num = 1;

//每个得分点的并列点个数
var same_point_num = {
    point1 : 1,
};

var question = {

};

var total_points = 0

$('#add_question').click(function() {
    console.log(9999999)
    $('#mask-kk').css({
        display: 'block',
        height: $(document).height()
    })
    var $Popup = $('#popup-kk');
    $Popup.css({
    left: ($('body').width() - $Popup.width()) / 2+ 'px',
    top: ($(window).height() - $Popup.height()) / 2 + $(window).scrollTop() + 'px',
    display: 'block'
    })
    $("body").css({overflow:"hidden"})
});

$('#close').click(function() {
    clear_all_text();
    clear_mask();
});

function clear_mask(){
    $('#mask-kk,#popup-kk').css('display', 'none');
    $("body").css({overflow:""});
}

//利用js提供的insertBefore及过滤器nextSibling\parentNode等，自己构建一个insertAfter
function insert_after(newElement, targetElement) {
    var parent = targetElement.parentNode;
    //如果要插入的目标元素是其父元素的最后一个元素节点，直接插入该元素
    //否则，在目标元素的下一个兄弟元素之前插入
    if (parent.lastChild == targetElement) {
        parent.appendChild(targetElement);
    } else {
        parent.insertBefore(newElement, targetElement.nextSibling);
    }
}

//$("input[id='add_same_point']").click(add_same_point);
$("#add_same_point1").click(add_same_point);
$("#pop_same_point1").click(pop_same_point);
$("input[id='add_another_point']").click(add_another_point);
$("input[id='pop_another_point']").click(pop_another_point);
$("#point1_score").bind('input propertychange',input_points);
$("#add_to_page").click(add_to_page);
$("#add_test").click(add_test);

function add_same_point() {
    var parentElement = $(this).parent()[0];
    same_point_num[parentElement.id]++;//point?
    var inputElement = document.createElement("input");
    var lastPoint = document.getElementById(parentElement.id + "_1");
    inputElement.setAttribute("id",parentElement.id + "_" + `${same_point_num[parentElement.id]}`);
    inputElement.setAttribute("placeholder","并列得分点" + (same_point_num[parentElement.id] - 1));
    parentElement.insertBefore(inputElement,lastPoint);

}

function pop_same_point(){
    var parentElement = $(this).parent()[0];
    if (same_point_num[parentElement.id] > 1) {
        var current_dom = document.getElementById(parentElement.id + "_" + `${same_point_num[parentElement.id]}`);
        parentElement.removeChild(current_dom);
        same_point_num[parentElement.id]--;
    }else{
        alert("至少有一个得分点！")
    }
}

function add_another_point(){
    point_num++;
    same_point_num['point'+ point_num ] = 1
    var liElement = document.createElement("li");
    var lastPoint = document.getElementById('point'+ (point_num-1));
    liElement.setAttribute("id","point"+`${point_num}`);
    var inner = `
                得分点${point_num}：
                <input id="point${point_num}_1" placeholder = "可添加并列得分点"></input>
                <input id="add_same_point${point_num}" type="button" value="+">
                <input id="pop_same_point${point_num}" type="button" value="-">
                <br>
                分值：<input id="point${point_num}_score" type="text" placeholder="这里是单个点的分值"></input>
                `;
    liElement.innerHTML = inner;
    insert_after(liElement,lastPoint);
    //给每个新添加的按钮中添加click事件
    $("#add_same_point" + point_num).click(add_same_point);
    $("#pop_same_point" + point_num).click(pop_same_point);
    //给每个新添加的数值input中添加blur事件
    $("#point"+ point_num +"_score").bind('input propertychange',input_points);
    //对得分点的改变需要更新总分值的显示
    show_total_points();
}

function pop_another_point(){
    var parentElement = $(this).parent()[0];
    if (point_num > 1) {
        var current_dom = document.getElementById("point" + `${point_num}`);
        parentElement.removeChild(current_dom);
        point_num--;
    }else{
        alert("至少有一个得分点！")
    }
    //对得分点的改变需要更新总分值的显示
    show_total_points();
}

//计算得分点总和同时显示出来
function show_total_points(){
    total_points = 0;
    for (var i = 1; i <= point_num;i++){
        total_points += Number($("#point"+i+"_score").val());
    };
    $("#total_points")[0].innerHTML = "总分值：" + total_points;
}
//输入每个得分点的分值
function input_points(){
    value = Number($(this).val());
    if (isNaN(value)){
        alert("不是有效分值！");
        $(this).val("");
        //清空之后也要显示总分值
        show_total_points()

    }
    else{
        show_total_points()
    }
}

//获取所有输入的文字
function get_all_text(){
    question.question_stem = $("#question_stem").val();
    //得分点循环
    for (var i = 1; i <= point_num;i++){
        question['point' + i] = {};
        question['point' + i].samePoints = [];
        question['point' + i].score = $("#point" + i + "_score").val();
        //平行得分点循环
        for (var j = 1;j <= same_point_num['point' + i];j++){
            question['point' + i].samePoints.push($("#point" + i + '_' + j).val());
        }
    }

}

//清除所有输入的文字
function clear_all_text(){
    //清除得分点，留一个即可
    for (var i = 2; i <= point_num;i++){
        $("#point"+i).remove();
    }
    //清除并列得分点
    for (var i = 2; i <= same_point_num.point1;i++){
        $('#point1_'+i).remove();
    }
    //初始化全局变量
    point_num = 1;
    same_point_num = {point1 : 1};
    question = {};
    $("#question_stem").val('');
    $("#point1_1").val('');
    $("#point1_score").val('');
    show_total_points();
}

//判断是否为非空字符串
function emptyString(str) {
    if(str === '' || str === null || str === undefined){
        return true;
    }else{
        return false;
    }
}

function trans_text_to_page(){
    var liElement = document.createElement("li");
    liElement.setAttribute("id", "question" + question_num);
    innerHTML = `
        <strong  id="question${question_num}_stem"> ${question.question_stem} （${total_points}分）</strong>
        <div>答案：</div><div id="question${question_num}_points"></div>
    `
    
    liElement.innerHTML = innerHTML;
    $("#added_items").append(liElement);

    for (var i = 1; i <= point_num;i++){
        var divElement = document.createElement("div");
        divElement.setAttribute("id","question"+ question_num +"_point" + i);
        divElement.innerHTML = `
            （${question['point' + i].score}分）
        `;
        $("#question"+ question_num +"_points").append(divElement);
        for (var j = 0;j <same_point_num['point' + i];j++){
            //console.log(question['point' + i].samePoints[j]);
            var divElement = document.createElement("div");
            divElement.setAttribute("id","question"+ question_num +"_point" + i + "_" + j);
            divElement.setAttribute("style","float:left");
            divElement.innerHTML = `
                ${question['point' + i].samePoints[j]} 或
            `;
            if (j === same_point_num['point' + i] - 1){
                divElement.innerHTML = `
                ${question['point' + i].samePoints[j]}
            `;
            }
            $("#question"+ question_num +"_point" + i).append(divElement);
        }
    }
    question_num++;
}

//添加题目到页面
function add_to_page(){
    var emptyInput = [];
    get_all_text();
    emptyInput.push(emptyString(question.question_stem));
    for (var i = 1; i <= point_num;i++){
        emptyInput.push(emptyString(question['point' + i].score))
        for (var j = 0;j < same_point_num['point' + i];j++){ //这里一定要注意数组从0开始取
            emptyInput.push(emptyString(question['point' + i].samePoints[j]));
        }
    }

    if(emptyInput.includes(true)){
        alert("有空白内容，请检查！");
    }
    else{
        trans_text_to_page();
        clear_all_text();
        clear_mask();
    }
}

//添加习题到数据库
function add_test(){

}