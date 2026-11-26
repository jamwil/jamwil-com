+++
title = "Pulling a Smartsheet table into Microsoft Excel using Power Query"
date = "2024-03-07T05:04:34Z"
[taxonomies]
tags = ["data", "excel", "power-query", "smartsheet"]
categories = ["Technology"]
+++

Well if you thought my first post in eight months would be exotic, go ahead and
smash that back button.

I use this technique when we have one-off assignments at work where I need a
quick and dirty web-based data store that several people can collaborate on, and
that can be easily queried in Excel without any intermediate infrastructure or
processing. This would be quite trivial if not for Smartsheet's intractible API
format.

Assuming you have a Smartsheet grid you want to mirror in Excel and that can be
refreshed on the fly, you'll need the sheet's ID and an API bearer token for a
user with viewer permissions.

In Excel, open Power Query and create a new query using the advanced editor.
**Make sure to replace `$SHEET_ID` and `$BEARER_TOKEN`**. The query will bring
in both your data and column headers.

{% raw %}
```
let
    Source = Json.Document(
        Web.Contents("https://api.smartsheet.com/2.0/sheets/$SHEET_ID", [
            Headers=[
                #"Content-Type"="application/json",
                Authorization="Bearer $BEARER_TOKEN"
            ]
        ])
    ),

    // Process rows
    RowsData = Source[rows],
    RowsTable = Table.FromList(RowsData, Splitter.SplitByNothing()),
    ExpandedRows = Table.ExpandRecordColumn(
        RowsTable,
        "Column1",
        {"id", "rowNumber", "expanded", "createdAt", "modifiedAt", "cells", "siblingId"},
        {"ID", "RowNumber", "Expanded", "CreatedAt", "ModifiedAt", "Cells", "SiblingId"}
    ),
    ExpandCells = Table.ExpandListColumn(ExpandedRows, "Cells"),
    ExpandedCellsDetails = Table.ExpandRecordColumn(
        ExpandCells,
        "Cells",
        {"columnId", "value", "displayValue"},
        {"ColumnID", "CellValue", "CellDisplayValue"}
    ),
    RemovedCellsMetaColumns = Table.RemoveColumns(
        ExpandedCellsDetails,
        {"ID", "Expanded", "CreatedAt", "ModifiedAt", "CellDisplayValue", "SiblingId"}
    ),
    PivotedCellsByColumnId = Table.Pivot(
        Table.TransformColumnTypes(RemovedCellsMetaColumns, {{"ColumnID", type text}}),
        List.Distinct(Table.TransformColumnTypes(RemovedCellsMetaColumns, {{"ColumnID", type text}})[ColumnID]),
        "ColumnID",
        "CellValue"
    ),
    CleanRowData = Table.RemoveColumns(PivotedCellsByColumnId, {"RowNumber"}),

    // Process columns
    ColumnsData = Source[columns],
    ColumnsTable = Table.FromList(ColumnsData, Splitter.SplitByNothing()),
    ExpandedColumns = Table.ExpandRecordColumn(
        ColumnsTable,
        "Column1",
        {"id", "title"},
        {"ColumnID", "ColumnTitle"}
    ),
    ColumnTitlesMapped = Table.Pivot(
        Table.TransformColumnTypes(ExpandedColumns, {{"ColumnID", type text}}),
        List.Distinct(Table.TransformColumnTypes(ExpandedColumns, {{"ColumnID", type text}})[ColumnID]),
        "ColumnID",
        "ColumnTitle"
    ),

    // Add headers
    CombinedDataTable = Table.Combine({ColumnTitlesMapped, CleanRowData}),
    FinalData = Table.PromoteHeaders(CombinedDataTable)

in
    FinalData
```
{% endraw %}

<!-- more -->
