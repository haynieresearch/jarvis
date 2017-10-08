select substr('0000000000' || state_id, -10, 10) as '' ,
substr('                    ' || domain, -20, 20) as '' ,
substr('                                                  ' || entity_id, -50, 50) as '' ,
substr('                         ' || state, -25, 25) as '' ,
substr('0000000000' || event_id, -10, 10) as '' ,
substr('                   ' || datetime(last_changed), -19, 19) as '' ,
substr('                   ' || datetime(last_updated), -19, 19) as '' ,
substr('                   ' || datetime(created), -19, 19) as '' 
from states;
