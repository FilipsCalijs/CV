function solution(str, ending){
    str = str.split("").reverse().join("");
    ending = ending.split("").reverse().join("");
    str = str.slice(0,ending.length);
    
    if (str == ending){
      return true
    } else {
      return false
    }
    
  }