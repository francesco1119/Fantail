/*    ==Scripting Parameters==

    Source Server Version : SQL Server 2016 (13.0.4001)
    Source Database Engine Edition : Microsoft SQL Server Enterprise Edition
    Source Database Engine Type : Standalone SQL Server

    Target Server Version : SQL Server 2016
    Target Database Engine Edition : Microsoft SQL Server Enterprise Edition
    Target Database Engine Type : Standalone SQL Server
*/

USE [ip2location]
GO

/****** Object:  Table [dbo].[GoogleDetails]    Script Date: 27/09/2017 10:46:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[GoogleDetails](
	[Place_ID] [nchar](50) NULL,
	[ID] [nchar](50) NULL,
	[Name] [nchar](100) NULL,
	[Street_Number] [nchar](50) NULL,
	[Street] [nchar](100) NULL,
	[Postal_Code] [nchar](50) NULL,
	[City] [nchar](100) NULL,
	[Area1] [nchar](100) NULL,
	[Area2] [nchar](100) NULL,
	[Country] [nchar](50) NULL,
	[CountryCode] [nchar](50) NULL,
	[Phone] [nchar](50) NULL,
	[Latitude] [nchar](50) NULL,
	[Longitude] [nchar](50) NULL,
	[Types] [varchar](max) NULL,
	[Rating] [nchar](50) NULL,
	[GoogleURL] [nchar](200) NULL,
	[Website] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
