# Github Crawler

this is a code for crawling the Github (using Scrapy spider). you should pate the link in the parameter URL and then use it, for example:
```bash
URL = 'https://github.com/tensorflow/models'
```
it can give you: comments of a pull and the code and changes of the code and ones who had changed a file and so on.
example:
```json
{
	"file": "https://github.com/rg3/youtube-dl/blob/master/docs/conf.py",
		"commits": [{
			"committer": "/TRox1972",
			"date": "2016-10-02T11:39:18Z"
			},
			{
			"committer": "/jaimeMF",
			"date": "2014-03-15T18:08:09Z"
			}]
},
```
```json
{
	"pull": "https://github.com/tensorflow/models/pull/6694",
	"pull_owner": "https://github.com/tfboyd",
	"file_code_comments": [{"file": "https://github.com/rg3/youtube-dl/blob/masterofficial/recommendation/ncf_keras_benchmark.py",
	"code": {
			"before": [-1, -1, -1, -1], "after": [107, 108, 109, 110], 
			"code_lines": ["", "    metrics.append({'name': 'hr_at_10',", "                    'value': stats['eval_hit_rate'],", "                    'min_value': 0.620,"]},
			"comments": [{
							"author": "https://github.com/seemuch",
							"date": "2019-04-29T14:31:32Z",
							"text": " \n             I think 0.620 might be a little high for min_val. I have seen values that are blow this. Like, 0.619. \n           "}]}],
			"committed_files": [{
							"file": "https://github.com/tensorflow/models/blob/master/official/recommendation/ncf_keras_benchmark.py",
							"date": "2019-04-29T21:03:56Z",
							"before": [105, 106, 107, -1, -1, 108, 109, 110, -1, 111, 112, 113],
			"after": [105, 106, 107, 108, 109, 110, 111, -1, 112, 113, 114, 115],
			"code_lines": [
				"    metrics.append({'name': 'exp_per_second',", "                    'value': stats['avg_exp_per_second']})",
				"",
				"    # Target is 0.625, but some runs are below that level. Until we have", 
				"    # multi-run tests, we have to accept a lower target.", 
				"    metrics.append({'name': 'hr_at_10',", "                    'value': stats['eval_hit_rate'],",
				"                    'min_value': 0.620,", "                    'min_value': 0.618,", 
				"                    'max_value': 0.635})", "", "    metrics.append({'name': 'train_loss',"], 
			"code_changes": [" ", " ", " ", "+", "+", " ", " ", "-", "+", " ", " ", " "]},
		{
			"file": "https://github.com/tensorflow/models/blob/master/official/recommendation/ncf_keras_benchmark.py",
			"date": "2019-04-29T19:58:08Z",
			"before": [20, 21, 22, 23, 24, 25, 26, 32, 33, 34, -1, 35, 36, 37, 66, 67, 68, 69, 70, -1, -1, 71, 72, 73, -1, 74, 75, 76, 103, 104, 105, 106, 107, 108,
						109, 110,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 111, 112, 113, 158, 159, 160, 161, 162, 163, -1, -1, -1, -1, 164, 165, 166],
			"after": [20, 21, 22, -1, 23, 24, 25, 31, 32, 33, 34, 35, 36, 37, 66, 67, 68, -1, -1, 69, 70, 71, 72, -1, 73, 74, 75, 76, 103, 104, 105, -1, -1, -1, -1,
						-1, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 166, 167, 168, -1, -1, -1, 169, 170, 171, 172, 173, 174, 175],
			"code_lines": ["the lines of code, too long to be shown"],
			"code_changes": [" ", " ", " ", "+", " ", " ", " ", " ", " ", " ", "-", " ", " ", "-", " ", " ", "-", "-", "-", "-", " ",
							" ", " "," ", " ", "+", " ", " ", " ", " ", " ", " ", "+", " ", " ", " ", " ", " ", " ", "+", " ", " ", " "]}]
}
```