create or replace function  SET_1187000(I_SET_ID int)
returns int
as
$body$
declare
ERRORCODE	INT := 0;
begin
/* Set name SET_AngularJS_Artifact*/
  insert into SET_Contents (SetId, ObjectId)
  select distinct I_SET_ID, o.OBJECT_ID
  from DSSAPP_ARTIFACTS o where o.OBJECT_TYPE in (1187014,1187016);
Return ERRORCODE;
END;
$body$
LANGUAGE plpgsql
/



