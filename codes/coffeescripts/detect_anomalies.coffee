# Description:
#   This is a test for making HTTP calls
#
# Commands:
#   hubot detect anomalies - a test to detect anomalies in the past 5 minutes.

child_process = require('child_process')
module.exports = (robot) ->
  robot.respond /detect anomalies/i, (msg) -> 
    comd = 'sh ~/my_hubot/bash/detect.sh'
    child_process.exec comd, (err, stdout, stderr) ->
      if err
        msg.send 'ERROR!'
      else
        sleep 5000
        robot.http("http://192.168.188.128:5000/")
          .get() (err, res, body) ->
            if(err)
              msg.send "ERROR1"
            else
              msg.send "Potential exceptions were detected at:\n\r#{body} in the past five minutes."

sleep = (ms)->
  start = new Date().getTime()
  continue while new Date().getTime() - start < ms

