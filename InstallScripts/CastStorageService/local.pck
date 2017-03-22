<?xml version="1.0" encoding="utf-8"?>
<Package PackName="PLUGIN_BPEL_LOCAL" Type="SPECIFIC" Version="1.0.0.0" SupportedServer="ALL" Display="ADG Metric Tree for BPEL" Description="" DatabaseKind="KB_LOCAL">
	<Include>
		<PackName>OBJSET</PackName>
		<Version>7.0.0</Version>
	</Include>
	<Exclude>
	</Exclude>
	<Install>
	</Install>
	<Update>
    </Update>
	<Refresh>
        <Step Type="PROC" File="set_local.sql"></Step>
		<Step Type="DATA" File="set_data.xml" Model="set_tables.xml" Scope="OBJSETINIT"></Step>
	</Refresh>
	<Remove>
	</Remove>
</Package>