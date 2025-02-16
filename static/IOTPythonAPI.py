from flask import Flask, request, jsonify
import mysql.connector
import requests
from datetime import timedelta, datetime
import json
import uuid

app = Flask(__name__);


@app.route('/apiv2/chart2/<siteid>/<item>/<StartDate>/<EndDate>', methods=['GET'])
def chart2(siteid, item, StartDate, EndDate):
    try:
        # print(StartDate);
        # print(EndDate);

        connection = mysql.connector.connect(
            host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        if connection.is_connected():
            cursor = connection.cursor();

            siteId = 'sf_data_log_' + str(siteid);
            sensorID = item.split(",");
            result = [];

            color = ["#0BC196", "#C1840B", "#6F43C4", "#1C77FF",
                     "#ED589D", "#8A00BA", "#FF5252", "#0091EA", "#66BB6A"];

            # print(sensorID);
            for sensor in range(len(sensorID)):
                # arr.append({"name": sensorID[a], "type": "line", "color": color[a], "data": []});

                currentSensor = {
                    "name": sensorID[sensor], "type": "line", "color": color[sensor], "data": []};

                # query = f"SELECT dl_create_date as 'datetime',a.dl_state as 'value' FROM {siteId} a WHERE a.dl_name='{sensorID[a]}' AND dl_type='1' AND dl_state not in ('9999','99999','999999','9999999','99999999',9999,99999,999999,9999999,99999999) and dl_create_date >(NOW()-INTERVAL {days} DAY) AND dl_create_date< NOW() group by sd_id,dl_state,DATE_FORMAT(`dl_create_date`, '%Y-%m-%d %H:%i') ORDER BY dl_id ASC";

                query = f"SELECT dl_create_date as 'datetime',a.dl_state as 'value' FROM {siteId} a WHERE a.dl_name='{sensorID[sensor]}' AND dl_type='1' AND dl_state not in ('9999','99999','999999','9999999','99999999',9999,99999,999999,9999999,99999999) and dl_create_date >= '{StartDate}'  and dl_create_date <= '{EndDate}' group by sd_id,dl_state,DATE_FORMAT(`dl_create_date`, '%Y-%m-%d %H:%i') ORDER BY dl_id ASC"

                # print(query);
                cursor.execute(query);
                records = cursor.fetchall();

                for row in records:
                    # arr[a]["data"].append({"x": str(row[0]), "y": float(row[1])});
                    currentSensor["data"].append(
                        {"x": str(row[0]), "y": float(row[1])});

                result.append(currentSensor);

            return jsonify(result);

    except Exception as e:
        print(str(e))

    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
            # print("connection closed");

# Custom Interval
@app.route('/apiv2/chart2HourlyInterval/<siteid>/<item>/<StartDate>/<EndDate>', methods=['GET'])
def chart2Interval(siteid, item, StartDate, EndDate):
    try:
        connection = mysql.connector.connect(
            host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        
        result = [];

        if connection.is_connected():
            cursor = connection.cursor();

            siteId = 'sf_data_log_' + str(siteid);
            sensorID = item.split(",");

            color = ["#0BC196", "#C1840B", "#6F43C4", "#1C77FF",
                     "#ED589D", "#8A00BA", "#FF5252", "#0091EA", "#66BB6A"];

            # print(sensorID);
            for sensor in range(len(sensorID)):
                
                
                currentSensor = currentSensor = currentSensor = {
                        "name": sensorID[sensor], "type": "line", "color": color[sensor], "data": []};
                
                query = f"SELECT dl_create_date as 'datetime',a.dl_state as 'value' FROM {siteId} a WHERE a.dl_name='{sensorID[sensor]}' AND dl_type='1' AND dl_state not in ('9999','99999','999999','9999999','99999999',9999,99999,999999,9999999,99999999) AND dl_create_date >= '{StartDate}' AND dl_create_date <= '{EndDate}'  group by sd_id,dl_state,DATE_FORMAT(`dl_create_date`, '%Y-%m-%d %H:%i') ORDER BY dl_id ASC";

                cursor.execute(query);
                records = cursor.fetchall();
                
                tempSensorData = [];

                for row in records:
                    tempSensorData.append( {"x": str(row[0]), "y": float(row[1])});

                if len(tempSensorData) > 0:
                    
                    maximum = tempSensorData[0]['y'];
                    minimum = tempSensorData[0]['y'];
                    total = 0;
                    
                    # Hourly
                    hour = memoryview(bytearray('00', 'ascii')).tobytes();

                    hourlyYSum, hourlyXCount = 0, 0;
                    for data in tempSensorData:
                        
                        if (data["y"] > maximum):
                            maximum = data['y'];
                            
                        if (data['y'] < minimum):
                            minimum = data['y'];
                            
                        total += data['y']; 
                        
                        hourlyYSum += data['y'];
                        hourlyXCount += 1;
                            
                        currDate = bytearray(data['x'], 'ascii');
                        memDate = memoryview(currDate)[14:16].tobytes();

                        if memDate == hour:
                            currentSensor["data"].append( {'x': data['x'], 'y': round(hourlyYSum/hourlyXCount, 2) });
                            hourlyYSum, hourlyXCount = 0, 0;
                    
                    avg = round(total / len(tempSensorData), 2);

                    
                    result.append(currentSensor);
                    
        return jsonify(result);

    except Exception as e:
        return 404;

    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
            

@app.route('/apiv2/chartInterval/<siteid>/<zone>/<token>/<language>/<item>/<StartDate>/<EndDate>/<Interval>/<ItemCount>', methods=['GET'])
def chartInterval(siteid, zone, token, language, item, StartDate, EndDate, Interval, ItemCount):
    try:
        connection = mysql.connector.connect(
            host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        
        result = [];
        
        if connection.is_connected():
            
            flag = True;
        
            if int(ItemCount) > 1:
                flag = False;
                
            
            cursor = connection.cursor();

            siteId = 'sf_data_log_' + str(siteid);
            sensorID = item.split(",");

            color = ["#0BC196", "#C1840B", "#6F43C4", "#1C77FF",
                     "#ED589D", "#8A00BA", "#FF5252", "#0091EA", "#66BB6A"];

            for sensor in range(len(sensorID)):
                isRain = False;
                lastRain = 0;
                rainHourlyCount = 0;
                hourlyRainAmt = 0;
                
                if "rain" in sensorID[sensor].lower().replace(" ", ""):
                    isRain = True;
                    
                currentSensor = currentSensor = {
                        "name": sensorID[sensor], "type": "line", "color": color[sensor], "data": []};
                
                if flag:
                    minimumJson = {"name": "Minimum", "type": "line", "color": "#FF5252", "data":[]};
                    maximumJson = {"name": "Maximum", "type": "line", "color": "#FF5252", "data":[]};
                
                query = f"SELECT dl_create_date as 'datetime',a.dl_state as 'value' FROM {siteId} a WHERE a.dl_name='{sensorID[sensor]}' AND dl_type='1' AND dl_state not in ('9999','99999','999999','9999999','99999999',9999,99999,999999,9999999,99999999) AND dl_create_date >= '{StartDate}' AND dl_create_date <= '{EndDate}'  group by sd_id,dl_state,DATE_FORMAT(`dl_create_date`, '%Y-%m-%d %H:%i') ORDER BY dl_id ASC";

                cursor.execute(query);
                records = cursor.fetchall();
                
                tempSensorData = [];

                for row in records:
                    tempSensorData.append( {"x": str(row[0]), "y": float(row[1])});

                if len(tempSensorData) > 0:
                    
                    if flag:
                        maximum = tempSensorData[0]['y'];
                        minimum = tempSensorData[0]['y'];
                        resetMinMax = False;

                    hour = memoryview(bytearray('00', 'ascii')).tobytes();
                    if Interval != "Hourly":
                        hourlyYSum, hourlyXCount = 0, 0;
                        
                    for data in tempSensorData:
                        # Reset raining sensor every hour
                        if isRain:
                            if data['y'] > 0:
                                rainHourlyCount += 1;
                                lastRain = data['y'];
                                hourlyRainAmt += data['y'];
                            
                        if Interval == "Daily" and flag:
                            if resetMinMax:
                                minimum, maximum = data['y'], data['y'];
                                resetMinMax = False;
                            
                            if data["y"] > maximum:
                                maximum = data['y']; 
                            elif data['y'] < minimum:
                                minimum = data['y'];
                        
                        if Interval != "Hourly" and not isRain:
                            hourlyYSum += data['y'];    
                            hourlyXCount += 1;
                            
                        currDate = bytearray(data['x'], 'ascii');
                        memDate = memoryview(currDate)[14:16].tobytes();
                                             
                        # Get hourly reading first for Daily, Monthly and Yearly
                        if (Interval != "Hourly"):
                            if memDate == hour:
                                if not isRain:
                                    currentSensor["data"].append( {'x': data['x'], 'y': round(hourlyYSum/hourlyXCount, 2)});
                                else:
                                    if rainHourlyCount > 0:
                                        currentSensor["data"].append( {'x': data['x'], 'y': round(hourlyRainAmt/rainHourlyCount, 2)});
                                    else:
                                        currentSensor["data"].append( {'x': data['x'], 'y': 0});
                                        
                                if Interval == "Daily" and flag:
                                    minimumJson["data"].append({'x': data['x'], 'y': minimum});
                                    maximumJson["data"].append({'x': data['x'], 'y': maximum});
                                    resetMinMax = True;
                                
                                hourlyYSum, hourlyXCount = 0, 0;
                        else:
                            if isRain:
                                currentSensor["data"].append({'x': data['x'], 'y': lastRain});                                
                            else:
                                currentSensor["data"].append({'x': data['x'], 'y': data['y']});
                                
                        if isRain and memDate == hour:
                            lastRain, rainHourlyCount, hourlyRainAmt = 0, 0, 0;
                    # Directly access the final result array
                    result.append(currentSensor);
                    
                    if Interval == "Daily" and flag:
                        result.append(minimumJson);
                        result.append(maximumJson);
                                   
        if Interval == "Daily" or Interval == "Hourly":            
            return jsonify(result);
        else:
            return processMonthlyYearly(result, Interval, flag);

    except Exception as e:
        print(str(e));
        return 404;

    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
            
def processMonthlyYearly(result, Interval, flag):
    ret = [];
    
    for i in result:
        curr = {"name": i["name"], "type": "line", "color":i["color"], "data":[]};
        
        if flag:
            minimumJson = {"name": "Minimum", "type": "line", "color": "#FF5252", "data":[]};
            maximumJson = {"name": "Maximum", "type": "line", "color": "#FF5252", "data":[]};
        
        dailyCount, dailySum = 0, 0;
        
        for data in i["data"]:
            currMonth = bytearray(data['x'], 'ascii');
            currMonth = memoryview(currMonth)[8:10].tobytes();
            
            if flag:
                maximum, minimum = data['y'], data['y'];
                resetMinMax = False;
                
            break;
        
        temp = False;
        for data in i["data"]:
            if not temp:
                tempMonth = data['x'];
                temp = True;
                
            dailySum += data["y"];
            dailyCount += 1;
            
            if Interval == "Monthly" and flag:
                if resetMinMax:
                    maximum, minimum = data['y'], data['y'];
                    resetMinMax = False;
                
                if data['y'] > maximum:
                    maximum = data['y'];
                elif data['y'] < minimum:
                    minimum = data['y'];
            
            latestMonth = memoryview(bytearray(data['x'], 'ascii'))[8:10].tobytes();
            
            if (latestMonth != currMonth):
                currMonth = latestMonth;
                curr["data"].append({'x': tempMonth, 'y': round(dailySum/dailyCount, 2)});
                
                if Interval == "Monthly" and flag:
                    minimumJson["data"].append({'x': tempMonth, 'y': minimum});
                    maximumJson["data"].append({'x': tempMonth, 'y': maximum});
                    resetMinMax = True;
                    
                tempMonth = data['x'];
                temp = True;
                dailyCount, dailySum = 0, 0;
                
        ret.append(curr);
        
        if Interval == "Monthly" and flag:
            ret.append(minimumJson);
            ret.append(maximumJson);
            
    if Interval == "Monthly":
        return jsonify(ret);
    else:
        return processYearly(ret, flag);
        
def processYearly(ret, flag):
    final = []
    for i in ret:
        curr = {"name": i["name"], "type": "line", "color":i["color"], "data":[]};
        
        if flag:
            minimumJson = {"name": "Minimum", "type": "line", "color": "#FF5252", "data":[]};
            maximumJson = {"name": "Maximum", "type": "line", "color": "#FF5252", "data":[]};
        
        MonthlyCount, MonthlySum = 0, 0;
        
        for data in i["data"]:
            currYear = bytearray(data['x'], 'ascii');
            currYear = memoryview(currYear)[5:7].tobytes();
            
            if flag:
                maximum, minimum = data['y'], data['y'];
                resetMinMax = False;
            break;
        
        temp = False;
        for data in i["data"]:
            if temp == False:
                tempYear = data["x"];
                temp = True;
                
            MonthlySum += data["y"];
            MonthlyCount += 1;
            
            if flag:
                if resetMinMax:
                    minimum, maximum = data['y'], data['y'];
                    resetMinMax = False;
                    
                if data['y'] > maximum:
                    maximum = data['y'];
                elif data['y'] < minimum:
                    minimum = data['y'];
            
            latestYear = memoryview(bytearray(data['x'], 'ascii'))[5:7].tobytes();
            
            if (latestYear != currYear):
                currYear = latestYear;
                curr["data"].append({'x': tempYear, 'y': round(MonthlySum/MonthlyCount, 2)});
                
                if flag:
                    minimumJson["data"].append({'x': tempYear, 'y': minimum});
                    maximumJson["data"].append({'x': tempYear, 'y': maximum});
                    resetMinMax = True;
                    
                tempYear = data['x'];
                temp = True;
                MonthlyCount, MonthlySum = 0, 0;
                
        final.append(curr);   
        
        if flag:
            final.append(minimumJson);
            final.append(maximumJson); 
        
    return jsonify(final);
                 
@app.route('/apiv2/sensors/<siteid>/<zone>/<token>/<language>')
def getSensor(siteid, zone, token, language):
    headers = {
    "Authorization": "Basic " + token,
    "Cache-Control": "no-cache",
    "Postman-Token": "dd2fff1d-3862-faee-c87d-8c6b76767c5e"};
    
    url = "http://10.80.10.6:3000/rest/items/Sensor";
    
    response = requests.get(url, headers=headers, timeout=10);
    
    if response.status_code == 200:
        return jsonify(response.json()), 200;
    
@app.route('/apiv2/addNewReport/<siteid>/<zone>/<token>/<language>/<payload>')
def addNewReport(siteid, zone, token, language, payload):
    
    headers = {
    "Authorization": "Basic " + token,
    "Cache-Control": "no-cache",
    "Postman-Token": "dd2fff1d-3862-faee-c87d-8c6b76767c5e"};
    
    try:
        connection = mysql.connector.connect(host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        
        if connection.is_connected():
            primaryKey = str(uuid.uuid4());
            
            cursor = connection.cursor();
            jsonData = json.loads(payload);
            
            cursor.execute("insert into sf_custom_report values(%s, %s, %s, %s, %s, %s);", (str(jsonData['name']), str(jsonData['sensor']), str(jsonData['createdBy']), jsonData['createdDateTime'], siteid.replace(" ", ""), primaryKey));
            connection.commit();
            
            if cursor.rowcount >= 1:
                return jsonify([]), 200;

    except Exception as e:
        print(e);
        return jsonify([]), 404;
    
    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
                        
@app.route('/apiv2/deleteCustomReport/<siteid>/<zone>/<token>/<language>/<uuid>')
def deleteCustomReport(siteid, zone, token, language, uuid):
    
    try:
        connection = mysql.connector.connect(host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        
        if connection.is_connected():
            cursor = connection.cursor();
            
            query = f"delete from sf_custom_report where uuid = '{uuid}';"
            cursor.execute(query);
            
            if cursor.rowcount > 0:
                connection.commit();
                return jsonify([]), 200;
            
    except Exception as e:
        return jsonify([]), 404;
    
    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
            

@app.route('/apiv2/getCustomReport/<siteid>/<zone>/<token>/<language>')
def getCustomReport(siteid, zone, token, language):
    headers = {
    "Authorization": "Basic " + token,
    "Cache-Control": "no-cache",
    "Postman-Token": "dd2fff1d-3862-faee-c87d-8c6b76767c5e"};
    
    try:
        connection = mysql.connector.connect(host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        
        if connection.is_connected():
            result = [];

            cursor = connection.cursor();
            
            siteid = siteid.replace(" ", "");
            
            query = f"SELECT ReportName, Sensor, CreatedBy, uuid, CreatedDateTime from sf_custom_report where SiteID = {siteid};"
            
            cursor.execute(query);
            records = cursor.fetchall();
            
            for row in records:
                resultData = {"title": row[0], "item": row[1], "type": row[2], "uuid": row[3], "createdDateTime": row[4]};
                result.append(resultData);
                
            return jsonify(result);
    
    except Exception as e:
        return jsonify([]), 404;
    
    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
            
@app.route('/apiv2/editCustomReport/<siteid>/<zone>/<token>/<language>/<title>/<sensorList>/<uuid>')
def editCustomReport(siteid, zone, token, language, title, sensorList, uuid):
    try:
        connection = mysql.connector.connect(host='10.80.10.5', database='iot_sf', user='iot_sf', password='mGwmgZsnipOenVIH');
        
        if connection.is_connected():
            print(title);
            print(sensorList);
            cursor = connection.cursor();
            
            query = f"update sf_custom_report set Sensor = '{sensorList}', ReportName = '{title}' where uuid = '{uuid}';";
            cursor.execute(query);
            
            if cursor.rowcount > 0:
                connection.commit();
                return jsonify([]), 200;
        
        
    except Exception as e:
        return jsonify([]), 404;
        
    finally:
        if connection.is_connected():
            cursor.close();
            connection.close();
    
    
                
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8884,debug=False, threaded=True)
