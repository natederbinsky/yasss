# Yet Another Static Site System (yasss)

The idea of this software is to support client-side websites via a minimal wrapper-structure around a Python-based templating engine ([Jinja](https://jinja.palletsprojects.com)). 

There is support for multiple sites via common templates as well as extensibility for developing new templates. A goal is to require minimal knowledge beyond standard web technologies (HTML, CSS, JS) and some small amount of Jinja, as well as to support a spectrum of coding style in the space of [(Python/JS) scripted, hand-coded (HTML)].

## Some Terms

- **Template**. A packaging of Jinja template/macro files, static resources (e.g., CSS, JS), and Python code/data to support a particular type of site.
   - **Resource**. A file to copy when instantiating a template (e.g., locally hosted js/css files).
   - **Data**. Arbitrary Python variables used to populate pages (via the Jinja templating engine).
   - **Global**. a variable, typically a function, supplied to the Jinja engine that becomes available to all Jinja files (template & site).
- **Site**. A customized instantiation of a template, including pages (that typically will extend a template's Jinja file), site-specific resources (e.g., images, downloads), Python code, and site-specific data.
   - **Build**. Integrate site & template code in order to output a set of pages & resources rendered via Jinja.

## Starting a Site
Let's assume a good template already exists...

1. Create a folder that will contain your site-specific pages and resources (think of this as the state of your site)...
   - Create at least one page in this folder based upon Jinja files available for your desired template.
      - The extends path should take the form: `TEMPLATE_NAME/FILE.JINJA`
   - Structure resources within this folder.
2. Create a Python file that calls the appropriate template function to build your site; each template will require various inputs, but typically...
   - **site_dir**: the path to the folder you created in step #1.
   - **destination**: the path to the folder in which to build your site (**note: this folder will be deleted prior to each build**).
   - **pages**: the list of pages (i.e., file names relative to the site folder) to render using Jinja.
   - **resources**: the list of files (relative to the site folder) to be copied to the destination.
   - **data**: site-specific data to make available to site pages.
   - **globals**: site-specific globals to make available to site pages.

### Typical Workflow
Once you have a site structure, your typical process is to...

1. Make edits to your Python file and/or the contents of your site folder.
   - Note: the `util` import has some common functions for producing markup in Python (that is typically then passed as data for inclusion in pages).
2. Run your Python file to re-build your site given the changes.
3. Open rendered pages in the destination using your web browser.

## Making a Template
1. Create a template folder to house resources and Jinja files.
2. (Optional, but useful.) Create a Python file with template-specific utility methods, including any customization of the site build process.
   - The `gen` import provides a general `build` function that template-specific builds can call.

Jinja has great documentation for [template designers](https://jinja.palletsprojects.com/en/3.0.x/templates/).
