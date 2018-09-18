USE [ip2location]
GO

/****** Object:  Table [dbo].[GoogleNearbySearch]    Script Date: 18/09/2018 21:20:43 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[GoogleNearbySearch](
	[Place_ID] [nvarchar](50) NOT NULL,
	[ID] [nvarchar](50) NULL,
	[Name] [nvarchar](100) NULL,
	[Latitude] [decimal](20, 8) NULL,
	[Longitude] [decimal](20, 8) NULL,
	[Rating] [decimal](2, 1) NULL,
	[Types] [nvarchar](max) NULL,
	[Vicinity] [nvarchar](max) NULL,
 CONSTRAINT [PK_Place_ID] PRIMARY KEY NONCLUSTERED 
(
	[Place_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


USE [ip2location]
GO

/****** Object:  Table [dbo].[GoogleDetails]    Script Date: 18/09/2018 21:20:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[GoogleDetails](
	[Place_ID] [nvarchar](50) NOT NULL,
	[ID] [nvarchar](50) NULL,
	[Name] [nvarchar](100) NULL,
	[Street_Number] [nchar](50) NULL,
	[Street] [nvarchar](100) NULL,
	[Postal_Code] [nvarchar](50) NULL,
	[City] [nvarchar](100) NULL,
	[Area1] [nvarchar](100) NULL,
	[Area2] [nvarchar](100) NULL,
	[Country] [nvarchar](50) NULL,
	[CountryCode] [char](3) NULL,
	[Phone] [nchar](30) NULL,
	[Latitude] [decimal](9, 6) NULL,
	[Longitude] [decimal](9, 6) NULL,
	[Types] [nvarchar](max) NULL,
	[Rating] [decimal](2, 1) NULL,
	[GoogleURL] [varchar](max) NULL,
	[Website] [varchar](max) NULL,
 CONSTRAINT [PK__GoogleDe__D5C5153D113DA6D1] PRIMARY KEY NONCLUSTERED 
(
	[Place_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
