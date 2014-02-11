
function show(elementId)
{
	document.getElementById(elementId).style.display = "block";
}

function hide(elementId)
{
	document.getElementById(elementId).style.display = "none";
}

function hideAll()
{
	hide("btnShowMaps");
	hide("btnHideMaps");
	hide("btnShowThMaps");
	hide("btnShowAccMaps");
	hide("accessMap");
	hide("thZoneMap");
}

function hideMaps()
{
	hideAll()
	show("btnShowMaps");

}

function showMaps()
{
	hideAll();
	showAccessMaps();
}

function showAccessMaps()
{
	hideAll();
	show("accessMap");
	show("btnShowThMaps");
	show("btnHideMaps");
}

function showThermalZoneMaps()
{
	hideAll();
	show("thZoneMap")
	show("btnShowAccMaps");
	show("btnHideMaps");
}

function init()
{
	showAccessMaps();
}
