### Location data

<table>
<thead>
<tr><th>Area Type</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>S</td><td><a href="https://s3.amazonaws.com/quandl-production-static/zillow/areas_state.txt">State</a></td></tr>
<tr><td>CO</td><td><a href="https://s3.amazonaws.com/quandl-production-static/zillow/areas_county.txt">County</a></td></tr>
<tr><td>M</td><td><a href="https://s3.amazonaws.com/quandl-production-static/zillow/areas_metro.txt">Greater Metropolitan Area</a></td></tr>
<tr><td>C</td><td><a href="https://s3.amazonaws.com/quandl-production-static/zillow/areas_city.txt">City</a></td></tr>
<tr><td>N</td><td><a href="https://s3.amazonaws.com/quandl-production-static/zillow/areas_neighborhood.txt">Neighborhood</a></td></tr>
<tr><td>Z</td><td>Zip Code</td></tr>
</tbody>
</table>

Data is for the United States of America. Each location code consists of one of the above area type abbreviations 
followed by an arbitrary numeric specifier, e.g.: 
 <ul> 
 <li>S34 - State of Nevada</li>
 <li>C11729 - City of Chicago, IL</li>  
 <li>Z01234 - Zip Code 01234 (zip codes numbers are the same)</li>
 </ul>
 
**location_code_urls.json** 
* _area_type_ - one of the Area Type codes
* _url_ - host with file of numeric specifiers and descriptions 

**location_codes.json** - storage of parsed location codes 
* _area_type_ - C
* _name_ - e.g. Chicago, IL
* _location_code_ - e.g. C11729

**metadata.json**
* _file_ - path to data file
* _last_update_ - DTG of last update