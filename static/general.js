/* A collection of general functions for use in WisumVareflyt
      - 19.05.16 by Jonas J. Solsvik*/



function sortbyNumber(array, colindex){
	/*Function sorts a 2d array by a numbered column.
		array[] array = has to be a 2d array [[],[]]
		int colindex = has to be an int 1,2,3,4,5,6 which is a valid index in the array.
	 */
	var sortedArray = [];
	sortedArray = array.sort(function(a,b){
		return parseInt(a[colindex]) - parseInt(b[colindex]);
	});
	return sortedArray;
};

function sortbyDate(array, colindex){
	var sortedArray = [];
	sortedArray = array.sort(function(a,b){
		return b[colindex]['$date'] - a[colindex]['$date'];
	});
	return sortedArray;

};


var kwords = '';
var kwordsLength = 0;
var wordsCorrect = 0;
var row = '';

function generalSearch (array, sentence, limitTo=-10000, onerow=false) {
    /* A function that searches any column in a 2d-array
      for any word in a string-sentence.
		
		array[] array = [[something,some more, even more],[bla, bla bla]]
			(2d array has to have a static number of columns)
		string sentence = "This is a sentencce 2345 +1#?=¤="
		int limitTo = 1  (index of column limited to)
		bool onerow = true/false
      	*/
    var trimmedArray = [];

    kwords = sentence.split(' ');
	kwordsLength = kwords.length;

    /*Loop through rows, and make the rows toString() for faster searching.*/
    for (i=0; i<array.length; i++){

    	if (limitTo >= 0){
    		/* Limit columns that are searched*/
    		row = array[i][limitTo].toString().toUpperCase();
    	} else {
        	row = array[i].toString().toUpperCase();
    	};

        for (j=0; j < kwordsLength; j++){
            if (row.indexOf(kwords[j].toUpperCase()) > -1){
                wordsCorrect += 1;
            };
        };
        /*console.log("Correct: " + wordsCorrect + '| kwordsLength: ' + kwordsLength)*/

        if (onerow){
        	if (wordsCorrect == kwordsLength){
            	trimmedArray.push(array[i]);
                wordsCorrect = 0;   
            	return trimmedArray;
        	};
        } else {
        	if (wordsCorrect == kwordsLength){
            	trimmedArray.push(array[i]);
        	};
        };
        wordsCorrect = 0;
    };
    return trimmedArray;
};



var dateTime = null;
var dateString = '';
var timeString = '';
var datetimeString = '';

function formatTime(datetime){

    /* Gets a "time since epoch in milliseconds number and converts to readable format.
      Params: int datetime = 123344536778 
      return: string resultstring = 04.04.2016 - 14:48 */

    datetime = new Date(datetime['$date']);

    dateString =            ('0' + datetime.getDate().toString()).slice(-2) + 
                    "."   + ('0' + datetime.getMonth().toString()).slice(-2) + 
                    "."   +        datetime.getFullYear().toString();

    timeString =            ('0' + datetime.getHours().toString()).slice(-2) + 
                    ":"   + ('0' + datetime.getMinutes().toString()).slice(-2);

    datetimeString = dateString + ' - ' + timeString;
    return datetimeString;
};  


function deepCopy(oldValue) {
  /* Deep copy hack of a JSON object */
  var newValue
  strValue = JSON.stringify(oldValue)
  return newValue = JSON.parse(strValue)
}


