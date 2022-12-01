<?php
  // 时间: 2022-10-26
  // 作者: DJW
  // 功能: 小管岛将数采和ais历史数据传到云端

  // 跨域解决
  header("Content-type:text/json;charset=UTF-8");
  // header("Access-Control-Allow-Origin:*");
  // 连接数据库
  $conn = new mysqli("127.0.0.1", "DataPusher", "DataPusher", "shandong_db") or die("连接失败!");
  mysqli_query($conn, "set character set 'utf8'");
  mysqli_set_charset($conn, 'utf8');
  // 获取json数据
  $input = file_get_contents("php://input");
  $input_json = json_decode($input);
  
  $id = $input_json->id;
  $times = $input_json->times;
  $station_name = $input_json->station_name;
  // $project_name = $input_json->project_name;
  

  // 判断是哪个表的数据
  if($station_name=="shucai"){
    // 数采------------------------------
    $c1 = $input_json->c1;
    $c2 = $input_json->c2;
    $c3 = $input_json->c3;
    $c4 = $input_json->c4;
    $c5 = $input_json->c5;
    $c6 = $input_json->c6;
    $c7 = $input_json->c7;
    $c8 = $input_json->c8;
    $c9 = $input_json->c9;
    $c10 = $input_json->c10;
    $c11 = $input_json->c11;
    $c12 = $input_json->c12;
    $c13 = $input_json->c13;
    $c14 = $input_json->c14;
    $c15 = $input_json->c15;
    $c16 = $input_json->c16;
    $c17 = $input_json->c17;
    $c18 = $input_json->c18;
    $c19 = $input_json->c19;
    $c20 = $input_json->c20;
    $c21 = $input_json->c21;
    $c22 = $input_json->c22;
    $c23 = $input_json->c23;
    $c24 = $input_json->c24;
    $c25 = $input_json->c25;
    $c26 = $input_json->c26;
    $c27 = $input_json->c27;
    $c28 = $input_json->c28;
    $c29 = $input_json->c29;
    
    $sql = "INSERT IGNORE INTO `xiaoguandao_shucai_tbl`(id,times,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29) 
    VALUES($id,'$times',$c1,$c2,$c3,$c4,$c5,$c6,$c7,$c8,$c9,$c10,$c11,$c12,$c13,$c14,$c15,$c16,$c17,$c18,$c19,$c20,$c21,$c22,$c23,$c24,$c25,$c26,$c27,$c28,$c29);";
    $result = mysqli_query($conn, $sql);
  }else if($station_name=="ais_history"){
    // ais历史------------------------------
    $mmsi = $input_json->mmsi;
    $lon = $input_json->lon;
    $lat = $input_json->lat;
    $speed = $input_json->speed;
    $course = $input_json->course;
    $heading = $input_json->heading;

    $sql = "INSERT IGNORE INTO `xiaoguandao_ais_history_tbl`(id,times,mmsi,lon,lat,speed,course,heading) 
    VALUES($id,'$times','$mmsi',$lon,$lat,$speed,$course,$heading)";
    $result = mysqli_query($conn, $sql);
  }else if($station_name=="tk009"){
    // GPS------------------------------
    $lon = $input_json->lon;
    $lat = $input_json->lat;

    $sql = "INSERT IGNORE INTO `xiaoguandao_tk009_tbl`(id,times,lon,lat) 
    VALUES($id,'$times',$lon,$lat)";
    $result = mysqli_query($conn, $sql);
  }else{
    http_response_code(500);
    echo json_encode("{'msg':'station_name error'}");
  }

  if($result){
    echo json_encode("{'msg':'$station_name success'}");
  }else{
    http_response_code(500);
    echo json_encode("{'msg': error'}");
  }
  ?>