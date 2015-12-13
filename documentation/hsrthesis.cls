\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hsrthesis}[2012/06/06 A LaTex template for HSR Thesis]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions

\LoadClass[a4paper]{report}
\RequirePackage{ifthen}
\RequirePackage{graphicx}
\newcommand{\nothing}{}

\renewcommand*\familydefault{\sfdefault}
\newcommand{\sectionbreak}{\clearpage} % new page before section

\usepackage{enumitem}
\setlist[enumerate]{itemsep=0mm}
\setlist[itemize]{itemsep=0mm}
\setlength{\intextsep}{0mm}

%Page Size
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Template definitions
\oddsidemargin = 0pt
\textwidth = 460pt
\marginparwidth = 0pt
\hoffset = -60pt
\topmargin = 0pt
\voffset = -40pt
\textheight = 700pt

% Including mostly used packages
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage{mathptmx}
\usepackage[scaled=0.85]{helvet}
\usepackage{hyperref}
\usepackage{array}
\usepackage[ngerman]{babel}
\usepackage{glossaries}
\usepackage{color}
\usepackage{wrapfig}
\usepackage{url}
\usepackage{float}
\usepackage{natbib}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{setspace} 
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{titlesec}
\usepackage{pdflscape}
\usepackage{pdfpages}
\usepackage{listings}
\usepackage{dirtree}
\usepackage[titletoc,toc,page]{appendix}
\usepackage[nottoc,numbib]{tocbibind}

%Title Styling
%\titlespacing{command}{left spacing}{before spacing}{after spacing}[right]
%%%%%%%%%%%%%%%%%%%%%%%
\titlespacing{\section}{0pt}{10pt}{6pt}
\titlespacing{\subsection}{0pt}{10pt}{6pt}
\titlespacing{\subsubsection}{0pt}{10pt}{6pt}
\titlespacing{\paragraph}{0pt}{10pt}{6pt}[6pt]

% Table Stylings
% http://tex.stackexchange.com/a/13748
%%%%%%%%%%%%%%%%%%%%

\newcommand*\heading[1]{\bfseries{#1}}
\newcommand*\beforeheading{\toprule}
\newcommand*\afterheading{\midrule}
\newcommand*\normalline{}
\newcommand*\lastline{\bottomrule}

% Desicion Table of Content
% own Table of content for desicions
%http://texblog.org/2008/07/13/define-your-own-list-of/
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{tocloft}
\newcommand\decision[1]{%
	\refstepcounter{decision}
	\par\noindent\textbf{Entscheid  \thedecision. #1 }
	\addcontentsline{dec}{decision}
	{\protect\numberline{\thechapter.\thedecision}#1 }\par}

\newcommand\listdecisionname{Verzeichnis der Entscheide}
\newlistof{decision}{dec}{\listdecisionname}

%Shell Stylings
%http://tex.stackexchange.com/questions/46953/unix-command-highlighting-latex
\lstdefinestyle{BashInputStyle}{
  language=bash,
  basicstyle=\small\sffamily,
  numbers=left,
  numberstyle=\tiny,
  numbersep=3pt,
  frame=tb,
  columns=fullflexible,
  backgroundcolor=\color{yellow!20},
  linewidth=0.9\linewidth,
  xleftmargin=0.1\linewidth
}

\newcommand*{\Package}[1]{\texttt{#1}}%

%Python Code Stylings
%http://tex.stackexchange.com/questions/83882/how-to-highlight-python-syntax-in-latex-listings-lstinputlistings-command
%%%%%%%%%%%%%%%%%%%%%%%
% Default fixed font does not support bold face
\DeclareFixedFont{\ttb}{T1}{txtt}{bx}{n}{9} % for bold
\DeclareFixedFont{\ttm}{T1}{txtt}{m}{n}{9}  % for normal

% Custom colors
\definecolor{deepblue}{rgb}{0,0,0.5}
\definecolor{deepred}{rgb}{0.6,0,0}
\definecolor{deepgreen}{rgb}{0,0.5,0}
\definecolor{lightblue}{RGB}{100,149,237}

\usepackage{listings}

% Python style for highlighting
\newcommand\pythonstyle{\lstset{
language=Python,
basicstyle=\ttm,
otherkeywords={self},             % Add keywords here
keywordstyle=\ttb\color{deepblue},
emph={MyClass,__init__},          % Custom highlighting
emphstyle=\ttb\color{deepred},    % Custom highlighting style
stringstyle=\color{deepgreen},
frame=tb,                         % Any extra options here
showstringspaces=false            % 
}}


% Python environment
\lstnewenvironment{python}[1][]
{
\pythonstyle
\lstset{#1}
}
{}

% Python for external files
\newcommand\pythonexternal[2][]{{
\pythonstyle
\lstinputlisting[#1]{#2}}}

% Python for inline
\newcommand\pythoninline[1]{{\pythonstyle\lstinline!#1!}}


% Titlepage
%%%%%%%%%%%

\if@titlepage
	\renewcommand{\maketitle}{
		\begin{titlepage}
		% Logos
		\begin{picture}(0,200)(0,-100)
      		\put(-60, -30){\includegraphics[height=30mm]{images/hsrlogo.png}}
		\end{picture}

		% title
		\begin{center}
			\Large\thesistype , \departement\\[2ex]
			\huge\thesistitle\\[2ex]
			\large\school\\[1ex]
			\normalsize\term\\
			\normalsize\thedate
			\vfill
		\end{center}

		\begin{minipage}{\textwidth}
			\begin{flushleft}
				\large
				\begin{tabular}[t]{ll}
				% Checking Autor(s)
				\ifthenelse{\equal{\thesisauthora}{}}{\message{blub}}{\ifthenelse{\equal{\thesisauthorb}{}}{\emph{Autor:} & \thesisauthora\\[3pt]}{\ifthenelse{\equal{\thesisauthorc}{}}{\emph{Autoren:} & \thesisauthora \ \& \thesisauthorb\\[3pt]}{\emph{Autoren:} & \thesisauthora \ \& \thesisauthorb \ \& \thesisauthorc\\[3pt]}}}
				% Checking Supporter
				\ifthenelse{\equal{\professor}{}}{\\}{\emph{Betreuer:} & \professor\\[3pt]}
					\emph{Arbeitsperiode:} & \timeperiode\\[3pt]
					\emph{Arbeitsumfang:} & \workload\\[3pt]
					\emph{Link:} & \url{\linktothesis}
				\end{tabular}
			\end{flushleft}
		\end{minipage}
\end{titlepage}%    
}
   \else
   \renewcommand{\maketitle}{%
     \begin{flushleft}
       \null\hfill
       \vskip 2cm
       \sffamily\bfseries\upshape\huge
       \@title\\
       \mdseries\upshape\large
       \vspace{.5em}%
       \@author, \@date\\
	% \rule{\textwidth}{.5mm}\\
     \end{flushleft}
     \@thanks
     \par
     \vskip 1cm
     }
   \fi