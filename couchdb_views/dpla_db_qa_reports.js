{
   "_id": "_design/qa_reports",
   "language": "javascript",
   "views": {
       "spec_type": {
           "map": "function(doc) { v = doc.sourceResource.specType; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(doc['id'], v[i]); }}}"
       },
       "spec_type_count": {
           "map": "function(doc) { v = doc.sourceResource.specType; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(v[i],1); }}}",
           "reduce": "_count"
       },
       "is_shown_at": {
           "map": "function(doc) { v = doc.isShownAt; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(doc['id'], v[i]); }}}"
       },
       "is_shown_at_count": {
           "map": "function(doc) { v = doc.isShownAt; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(v[i],1); }}}",
           "reduce": "_count"
       },
       "title": {
           "map": "function(doc) { v = doc.sourceResource.title; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(doc['id'], v[i]); }}}"
       },
       "title_count": {
           "map": "function(doc) { v = doc.sourceResource.title; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(v[i],1); }}}",
           "reduce": "_count"
       },
       "creator": {
           "map": "function(doc) { v = doc.sourceResource.creator; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(doc['id'], v[i]);}}}"
       },
       "creator_count": {
           "map": "function(doc) { v = doc.sourceResource.creator; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "publisher": {
           "map": "function(doc) { v = doc.sourceResource.publisher; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "publisher_count": {
           "map": "function(doc) { v = doc.sourceResource.publisher; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],i);}}}",
           "reduce": "_count"
       },
       "dates": {
           "map": "function(doc) { v = doc.sourceResource.date; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i].displayDate+' ('+v[i].begin+' to '+v[i].end+')');}}}"
       },
       "dates_count": {
           "map": "function(doc) { v = doc.sourceResource.date; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i].displayDate+' ('+v[i].begin+' to '+v[i].end+')',1);}}}",
           "reduce": "_count"
       },
       "description": {
           "map": "function(doc) { v = doc.sourceResource.description; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "description_count": {
           "map": "function(doc) { v = doc.sourceResource.description; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "format": {
           "map": "function(doc) { v = doc.sourceResource.format; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "format_count": {
           "map": "function(doc) { v = doc.sourceResource.format; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "type": {
           "map": "function(doc) { v = doc.sourceResource.type; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "type_count": {
           "map": "function(doc) { v = doc.sourceResource.type; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "subject": {
           "map": "function(doc) { v = doc.sourceResource.subject; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i].name);}}}"
       },
       "subject_count": {
           "map": "function(doc) { v = doc.sourceResource.subject; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i].name,1);}}}",
           "reduce": "_count"
       },
       "spatial_state": {
           "map": "function(doc) { v = doc.sourceResource.spatial; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('state' in v[i]) {emit(doc['id'], v[i].state)};}}}"
       },
       "spatial_state_count": {
           "map": "function(doc) { v = doc.sourceResource.spatial; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('state' in v[i]) {emit(v[i].state,1)};}}}",
           "reduce": "_count"
       },
       "spatial_name": {
           "map": "function(doc) { v = doc.sourceResource.spatial; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('name' in v[i]) {emit(doc['id'], v[i].name)};}}}"
       },
       "spatial_name_count": {
           "map": "function(doc) { v = doc.sourceResource.spatial; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('name' in v[i]) {emit(v[i].name,1)};}}}",
           "reduce": "_count"
       },
       "state_located_in_state": {
           "map": "function(doc) { v = doc.sourceResource.stateLocatedIn; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('state' in v[i]) {emit(doc['id'], v[i].state)};}}}"
       },
       "state_located_in_state_count": {
           "map": "function(doc) { v = doc.sourceResource.stateLocatedIn; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('state' in v[i]) {emit(v[i].state,1)};}}}",
           "reduce": "_count"
       },
       "state_located_in_name": {
           "map": "function(doc) { v = doc.sourceResource.stateLocatedIn; if (vt) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('name' in v[i]) {emit(doc['id'], v[i].name)};}}}"
       },
       "state_located_in_name_count": {
           "map": "function(doc) { v = doc.sourceResource.stateLocatedIn; if (vt) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {if ('name' in v[i]) {emit(v[i].name,1)};}}}",
           "reduce": "_count"
       },
       "rights": {
           "map": "function(doc) { v = doc.sourceResource.rights; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "rights_count": {
           "map": "function(doc) { v = doc.sourceResource.rights; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "provider": {
           "map": "function(doc) { v = doc.provider; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('name' in v[i]) {emit(doc['id'], v[i].name);}}}}"
       },
       "provider_count": {
           "map": "function(doc) { v = doc.provider; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('name' in v[i]) {emit(v[i].name,1);}}}}",
           "reduce": "_count"
       },
       "data_provider": {
           "map": "function(doc) { v = doc.dataProvider; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "data_provider_count": {
           "map": "function(doc) { v = doc.dataProvider; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "collection_title": {
           "map": "function(doc) { v = doc.sourceResource.collection; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('title' in v[i]) {emit(doc['id'], v[i]['title']);}}}}"
       },
       "collection_title_count": {
           "map": "function(doc) { v = doc.sourceResource.collection; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('title' in v[i]) {emit(v[i]['title'],1);}}}}",
           "reduce": "_count"
       },
       "collection_description": {
           "map": "function(doc) { v = doc.sourceResource.collection; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('description' in v[i]) {emit(doc['id'], v[i]['description']);}}}}"
       },
       "collection_description_count": {
           "map": "function(doc) { v = doc.sourceResource.collection; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('description' in v[i]) {emit(v[i]['description'],1);}}}}",
           "reduce": "_count"
       },
       "contributor": {
           "map": "function(doc) { v = doc.sourceResource.contributor; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "contributor_count": {
           "map": "function(doc) { v = doc.sourceResource.contributor; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "language_name": {
           "map": "function(doc) { v = doc.sourceResource.language; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('name' in v[i]) {emit(doc['id'], v[i].name);}}}}"
       },
       "language_name_count": {
           "map": "function(doc) { v = doc.sourceResource.language; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('name' in v[i]) {emit(v[i].name,1);}}}}",
           "reduce": "_count"
       },
       "language_iso": {
           "map": "function(doc) { v = doc.sourceResource.language; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('iso639_3' in v[i]) {emit(doc['id'], v[i]['iso639_3']);}}}}"
       },
       "language_iso_count": {
           "map": "function(doc) { v = doc.sourceResource.language; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) { if ('iso639_3' in v[i]) {emit(v[i]['iso639_3'],1);}}}}",
           "reduce": "_count"
       },
       "temporal": {
           "map": "function(doc) { v = doc.sourceResource.temporal; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i].displayDate+' ('+v[i].begin+' to '+v[i].end+')');}}}"
       },
       "temporal_count": {
           "map": "function(doc) { v = doc.sourceResource.temporal; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i].displayDate+' ('+v[i].begin+' to '+v[i].end+')',1);}}}",
           "reduce": "_count"
       },
       "is_part_of": {
           "map": "function(doc) { v = doc.sourceResource.isPartOf; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "is_part_of_count": {
           "map": "function(doc) { v = doc.sourceResource.isPartOf; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "relation": {
           "map": "function(doc) { v = doc.sourceResource.relation; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "relation_count": {
           "map": "function(doc) { v = doc.sourceResource.relation; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "extent": {
           "map": "function(doc) { v = doc.sourceResource.extent; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "extent_count": {
           "map": "function(doc) { v = doc.sourceResource.extent; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       },
       "identifier": {
           "map": "function(doc) { v = doc.sourceResource.identifier; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(doc['id'], v[i]);}}}"
       },
       "identifier_count": {
           "map": "function(doc) { v = doc.sourceResource.identifier; if (v) { if (v.constructor.toString().indexOf('Array') == -1) { v = new Array(v); } for (i=0; i<v.length; i++) {emit(v[i],1);}}}",
           "reduce": "_count"
       }
   },
   "lists": {
       "csv": "function(head, req) { start({'headers': {'Content-Type': 'text/csv'}});var row; while (row = getRow()) { send(row.key + ',' + row.value + '\\n'); }}",
       "count_csv": "function(head, req) { start({'headers': {'Content-Type': 'text/csv'}});var row; while (row = getRow()) { send(row.key + ',' + row.value + '\\n'); }}"
   }
}
