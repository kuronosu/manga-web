
const leftPad = n => `0${n}`.substr(-2)

// function leftPad (number) {
//   number = number.toString()
//   const pad = '00'
//   return '00'.substring(0, '00'.length - number.length) + number
// }

const formattedTime = secs => {
  const minutes = ~~(secs/60)
  const hours = ~~(minutes/60)
  
  const secsf = leftPad(~~(secs%60))
  const minutesf = leftPad(~~(minutes%60))
  const hoursf = leftPad(~~(hours%24))
  const daysf = leftPad(~~(hours/24))

  let timeString
  if (daysf !== '00') {
    timeString = `${daysf}:${hoursf}:${minutesf}:${secsf}`
  } else if (hoursf !== '00') {
    timeString = `${hoursf}:${minutesf}:${secsf}`
  } else {
    timeString = `${minutesf}:${secsf}`
  }

  return timeString
}

const TimeUtils = {
    formattedTime,
    leftPad
}

export default TimeUtils
