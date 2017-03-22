<?xml version="1.1" encoding="UTF-8" ?>
<Package PackName="ADG_METRIC_TREE_BPEL" Type="INTERNAL" Version="7.3.4.1" SupportedServer="ALL" Display="ADG Metric Tree for BPEL" DatabaseKind="KB_CENTRAL" Description="">
	<Include>
	</Include>
	<Exclude>
	</Exclude>
	<Install>
    </Install>
	<Update>
    </Update>
	<Refresh>
		<Step Type="DATA" File="ADG_ConfigData.xml" Model="..\assessment_model_tables.xml" Scope="BPELScope"></Step>
	</Refresh>
	<Remove>
	</Remove>
</Package>