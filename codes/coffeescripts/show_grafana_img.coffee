# Description:
#   This is a test.
#
# Commands:
#   hubot showImg - Reply with test.png!

# use child_process to run a shell script file
child_process = require('child_process')

module.exports = (robot) ->
  robot.hear /showImg/i, (msg) ->	
    # generate a random number to name a new image 
    count = Math.ceil(Math.random()*1000000)
    comd = '~/my_hubot/bash/handlers/x' + ' ' + count  
    child_process.exec comd, (err, stdout, stderr) ->
      if err
        msg.send 'ERROR!'
      else
        sleep 5000
        # return the required Grafana image url
        msg.send 'https://raw.githubusercontent.com/170226/IOM/master/Grafana-images/t' + count + '.png'

# wait 5 seconds for running the shell script file
sleep = (ms)->
  start = new Date().getTime()
  continue while new Date().getTime() - start < ms