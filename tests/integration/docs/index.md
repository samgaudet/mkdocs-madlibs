# pytest cases

## Simple example

```madlibs
python
~~~
print("Hello, ___NAME___, welcome to MkDocs Mad Libs!")
```

## Multiple keywords

```madlibs
terraform
~~~
resource "google_project_iam_member" "project" {
  project = "___PROJECT_ID___"
  role    = "roles/___ROLE___"
  member  = "user:___EMAIL___"
}
```

## Simple example but with carets

```madlibs
python
~~~
print("Hello, ^^^NAME^^^, welcome to MkDocs Mad Libs!")
```

## Plain text example

```madlibs
text
~~~
"___EXCLAMATION___!" he said ___ADVERB___ as he jumped into his convertible ___NOUN___ and drove off with his ___ADJECTIVE___ wife.
```
