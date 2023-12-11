# Changelog

### [0.14.1](https://www.github.com/bihealth/clinvar-this/compare/v0.14.0...v0.14.1) (2023-12-11)


### Bug Fixes

* serialization of counter dict ([#174](https://www.github.com/bihealth/clinvar-this/issues/174)) ([06caa81](https://www.github.com/bihealth/clinvar-this/commit/06caa81c8f62cad5779fa62479474c52ca5c4a5d))

## [0.14.0](https://www.github.com/bihealth/clinvar-this/compare/v0.13.1...v0.14.0) (2023-12-11)


### Features

* adding async client code via switch to httpx ([#167](https://www.github.com/bihealth/clinvar-this/issues/167)) ([#170](https://www.github.com/bihealth/clinvar-this/issues/170)) ([7b76770](https://www.github.com/bihealth/clinvar-this/commit/7b76770fa3423a0651b5068edc59ec0a8e8588af))
* switch from attrs to pydantic ([#166](https://www.github.com/bihealth/clinvar-this/issues/166)) ([#168](https://www.github.com/bihealth/clinvar-this/issues/168)) ([d84db77](https://www.github.com/bihealth/clinvar-this/commit/d84db77ac2f33fc9c40c4a151fa730089b2f1788))
* updating to latest upstream JSON schemas ([#173](https://www.github.com/bihealth/clinvar-this/issues/173)) ([f5da1fc](https://www.github.com/bihealth/clinvar-this/commit/f5da1fc02f20d3f34674b037f3f4068d4bf5cec8))
* write out RCV/VCV version in extract_vars and phenotype_link ([#159](https://www.github.com/bihealth/clinvar-this/issues/159)) ([#172](https://www.github.com/bihealth/clinvar-this/issues/172)) ([534cba1](https://www.github.com/bihealth/clinvar-this/commit/534cba1d96f5f4c80ee7a744a847224942ad1561))


### Bug Fixes

* adding support for "no classification from unflagged records" review status ([#171](https://www.github.com/bihealth/clinvar-this/issues/171)) ([f144e74](https://www.github.com/bihealth/clinvar-this/commit/f144e7456f6177ee52e53f32e4940ab1b38ab68f))

### [0.13.1](https://www.github.com/bihealth/clinvar-this/compare/v0.13.0...v0.13.1) (2023-12-04)


### Bug Fixes

* pinning python to 3.11 in release for setuptools ([#164](https://www.github.com/bihealth/clinvar-this/issues/164)) ([afb6035](https://www.github.com/bihealth/clinvar-this/commit/afb60355e347449f107490d5eab351e8291e6d7a))

## [0.13.0](https://www.github.com/bihealth/clinvar-this/compare/v0.12.0...v0.13.0) (2023-12-04)


### Features

* adapt to ClinVar public XML update ([#162](https://www.github.com/bihealth/clinvar-this/issues/162)) ([8d90a36](https://www.github.com/bihealth/clinvar-this/commit/8d90a36fd4acfca0fd11fcfb0673f16efbce56b3))

## [0.12.0](https://www.github.com/bihealth/clinvar-this/compare/v0.11.0...v0.12.0) (2023-10-18)


### Features

* include VCV and title in "clinvar-data extract-vars" ([#152](https://www.github.com/bihealth/clinvar-this/issues/152)) ([c3e1bf2](https://www.github.com/bihealth/clinvar-this/commit/c3e1bf212643993ef0898f8ef28f4d0a973fcf7f))

## [0.11.0](https://www.github.com/bihealth/clinvar-this/compare/v0.10.2...v0.11.0) (2023-10-06)


### Features

* Adding Clinvar Accession to TSV input ([#146](https://www.github.com/bihealth/clinvar-this/issues/146)) ([1ef8b8f](https://www.github.com/bihealth/clinvar-this/commit/1ef8b8f7784c729a1247a8b7e0522a4e262657c8))
* Implement Pubmed IDs in tsv import format ([#143](https://www.github.com/bihealth/clinvar-this/issues/143)) ([9473380](https://www.github.com/bihealth/clinvar-this/commit/9473380191290edea046bd42d72df9b7c905f9e0))
* Support multiple condition types and multiple conditions ([#147](https://www.github.com/bihealth/clinvar-this/issues/147)) ([f972356](https://www.github.com/bihealth/clinvar-this/commit/f972356c11a94a03d7545bfb9d1ffb889cef112b))


### Bug Fixes

* mypy linting of tests ([#144](https://www.github.com/bihealth/clinvar-this/issues/144)) ([ee1fc5d](https://www.github.com/bihealth/clinvar-this/commit/ee1fc5d98026c4c5c3c248eca4e0907f21d45f0e))


### Documentation

* Update docs on file formats and fixing errors ([#150](https://www.github.com/bihealth/clinvar-this/issues/150)) ([0b9efc6](https://www.github.com/bihealth/clinvar-this/commit/0b9efc6640ffd4a814b1b5f8814589a9c6b65048))

### [0.10.2](https://www.github.com/bihealth/clinvar-this/compare/v0.10.1...v0.10.2) (2023-09-11)


### Bug Fixes

* typo accession => accession ([#135](https://www.github.com/bihealth/clinvar-this/issues/135)) ([9ac72a2](https://www.github.com/bihealth/clinvar-this/commit/9ac72a283873ba446d468cad597854e53a64689e))

### [0.10.1](https://www.github.com/bihealth/clinvar-this/compare/v0.10.0...v0.10.1) (2023-09-11)


### Bug Fixes

* properly write out variants to JSONL ([#133](https://www.github.com/bihealth/clinvar-this/issues/133)) ([17b7e5c](https://www.github.com/bihealth/clinvar-this/commit/17b7e5c7250a16edbf361c721a9af4ff58c1402e))

## [0.10.0](https://www.github.com/bihealth/clinvar-this/compare/v0.9.0...v0.10.0) (2023-09-08)


### Features

* write out HGNC identifier with variants ([#130](https://www.github.com/bihealth/clinvar-this/issues/130)) ([#131](https://www.github.com/bihealth/clinvar-this/issues/131)) ([ea33100](https://www.github.com/bihealth/clinvar-this/commit/ea33100e4af3329fb7e3018be0a2c8d215678924))

## [0.9.0](https://www.github.com/bihealth/clinvar-this/compare/v0.8.0...v0.9.0) (2023-09-08)


### Features

* write assessment to extract variants ([#128](https://www.github.com/bihealth/clinvar-this/issues/128)) ([dd72c90](https://www.github.com/bihealth/clinvar-this/commit/dd72c90a68f0e2cbd0306301de77985c0acb521e))


### Bug Fixes

* normalizing molecular consequence ([#126](https://www.github.com/bihealth/clinvar-this/issues/126)) ([c2a72cf](https://www.github.com/bihealth/clinvar-this/commit/c2a72cfcaea94752fdb8e278bc0a6d48748650a6))

## [0.8.0](https://www.github.com/bihealth/clinvar-this/compare/v0.7.0...v0.8.0) (2023-09-08)


### Features

* variant extraction ([#124](https://www.github.com/bihealth/clinvar-this/issues/124)) ([c7bb7c9](https://www.github.com/bihealth/clinvar-this/commit/c7bb7c9a2376d37b512b494631cf62dfcc23b19b))

## [0.7.0](https://www.github.com/bihealth/clinvar-this/compare/v0.6.0...v0.7.0) (2023-09-07)


### Features

* writing out clinical significance in gene-to-phenotype link ([#121](https://www.github.com/bihealth/clinvar-this/issues/121)) ([1c65fc6](https://www.github.com/bihealth/clinvar-this/commit/1c65fc6b9599a41810da4d020a84704e9a3f8c8c))

## [0.6.0](https://www.github.com/bihealth/clinvar-this/compare/v0.5.0...v0.6.0) (2023-09-07)


### Features

* write out organisation and local key to phenotype gene link ([#119](https://www.github.com/bihealth/clinvar-this/issues/119)) ([f87facc](https://www.github.com/bihealth/clinvar-this/commit/f87facc5b2e2754d5a4825ea8af3528ab0b4b0fe))

## [0.5.0](https://www.github.com/bihealth/clinvar-this/compare/v0.4.1...v0.5.0) (2023-09-07)


### Features

* allow read/write .gz everywhere ([#116](https://www.github.com/bihealth/clinvar-this/issues/116)) ([d3b658e](https://www.github.com/bihealth/clinvar-this/commit/d3b658e820953c38f7bc2b0727924490fc19ad8f))

### [0.4.1](https://www.github.com/bihealth/clinvar-this/compare/v0.4.0...v0.4.1) (2023-09-06)


### Bug Fixes

* adding clinvar_data to built package ([#114](https://www.github.com/bihealth/clinvar-this/issues/114)) ([4a78256](https://www.github.com/bihealth/clinvar-this/commit/4a78256a9a2f04a88472aa9b9617601e1b5c61f0))

## [0.4.0](https://www.github.com/bihealth/clinvar-this/compare/v0.3.0...v0.4.0) (2023-09-06)


### Features

* add command to extract gene-to-phenotype links ([#104](https://www.github.com/bihealth/clinvar-this/issues/104)) ([#106](https://www.github.com/bihealth/clinvar-this/issues/106)) ([b3b323a](https://www.github.com/bihealth/clinvar-this/commit/b3b323a2e440d4e4e34c9895f7e0b39b5425fdd7))
* adding --version option ([#110](https://www.github.com/bihealth/clinvar-this/issues/110)) ([7f3b091](https://www.github.com/bihealth/clinvar-this/commit/7f3b0917e39144b0b2fbbf760337ac16299500af))
* adding command to generate per-gene impact report ([#102](https://www.github.com/bihealth/clinvar-this/issues/102)) ([#103](https://www.github.com/bihealth/clinvar-this/issues/103)) ([c86a5c7](https://www.github.com/bihealth/clinvar-this/commit/c86a5c721ac5b089d63301a7ce40c0eea552b209))
* adding missing clinvar measure set ([#109](https://www.github.com/bihealth/clinvar-this/issues/109)) ([f0f64e0](https://www.github.com/bihealth/clinvar-this/commit/f0f64e0036a8b73eb6add02f81fcb54768b0b35f))
* adding support for parsing ClinVar XML ([#99](https://www.github.com/bihealth/clinvar-this/issues/99)) ([#100](https://www.github.com/bihealth/clinvar-this/issues/100)) ([c673f7d](https://www.github.com/bihealth/clinvar-this/commit/c673f7db8d94f0c05c1acd4c413e060db54a8649))
* command to extract variants per ACMG class and freq. ([#107](https://www.github.com/bihealth/clinvar-this/issues/107)) ([#108](https://www.github.com/bihealth/clinvar-this/issues/108)) ([c623f6d](https://www.github.com/bihealth/clinvar-this/commit/c623f6d804e7f9579b0cd8f15b086b066aef6338))


### Bug Fixes

* making conversion more robust, indicate errors ([#105](https://www.github.com/bihealth/clinvar-this/issues/105)) ([8333aea](https://www.github.com/bihealth/clinvar-this/commit/8333aea26cdc07b4467fa9ca56ea86eda642dd30))

## [0.3.0](https://www.github.com/bihealth/clinvar-this/compare/v0.2.1...v0.3.0) (2023-09-04)


### Features

* removing versioneer in favour of version from release-please ([#95](https://www.github.com/bihealth/clinvar-this/issues/95)) ([5b922bb](https://www.github.com/bihealth/clinvar-this/commit/5b922bb0a1fef23426cc73890db3f0868d668947))


### Bug Fixes

* using varfish-bot token for release-please ([#97](https://www.github.com/bihealth/clinvar-this/issues/97)) ([35fad52](https://www.github.com/bihealth/clinvar-this/commit/35fad5261210e8dfadc1e93fe151f4e885fb843b))

### [0.2.1](https://www.github.com/bihealth/clinvar-this/compare/v0.2.0...v0.2.1) (2023-03-17)


### Bug Fixes

* fixing strucvar export ([#84](https://www.github.com/bihealth/clinvar-this/issues/84)) ([1050a67](https://www.github.com/bihealth/clinvar-this/commit/1050a67edff50150da955f0e5364148c82b46902))
* sequence variant export ([#82](https://www.github.com/bihealth/clinvar-this/issues/82)) ([0fe3fb9](https://www.github.com/bihealth/clinvar-this/commit/0fe3fb9b4ec783218a408926007bb7370c70be64))

## [0.2.0](https://www.github.com/bihealth/clinvar-this/compare/v0.1.0...v0.2.0) (2023-03-15)


### Features

* add support for SV TSV files ([#75](https://www.github.com/bihealth/clinvar-this/issues/75)) ([#78](https://www.github.com/bihealth/clinvar-this/issues/78)) ([d4fffce](https://www.github.com/bihealth/clinvar-this/commit/d4fffce3772ed33c9d12c81b983e3e152f0c2d83))


### Documentation

* add badges to readme ([#65](https://www.github.com/bihealth/clinvar-this/issues/65)) ([207038c](https://www.github.com/bihealth/clinvar-this/commit/207038ccfa2473e09f283903e9c2a3cd249e2f30))
* adding file format documentation ([#71](https://www.github.com/bihealth/clinvar-this/issues/71)) ([3a04ffd](https://www.github.com/bihealth/clinvar-this/commit/3a04ffddd50ab21c52d3d2fe281d96ac30c505cb))
* extending docs; getting started from README ([#44](https://www.github.com/bihealth/clinvar-this/issues/44)) ([#68](https://www.github.com/bihealth/clinvar-this/issues/68)) ([77892f0](https://www.github.com/bihealth/clinvar-this/commit/77892f0fdaf158ed77c126f0aae11b12457c6043))
* updating docs introduction section ([#67](https://www.github.com/bihealth/clinvar-this/issues/67)) ([d6c865b](https://www.github.com/bihealth/clinvar-this/commit/d6c865b28db14e217c839239940bf9fe4fdcd5ed))

## 0.1.0 (2022-12-02)


### Features

* add basic config management in CLI ([#32](https://www.github.com/bihealth/clinvar-this/issues/32)) ([#33](https://www.github.com/bihealth/clinvar-this/issues/33)) ([c903546](https://www.github.com/bihealth/clinvar-this/commit/c903546751fe6c59fcc20770b6a1ad1ac88fbd86))
* add functions for managing batch data ([#34](https://www.github.com/bihealth/clinvar-this/issues/34), [#37](https://www.github.com/bihealth/clinvar-this/issues/37)) ([#35](https://www.github.com/bihealth/clinvar-this/issues/35)) ([0c7e0f9](https://www.github.com/bihealth/clinvar-this/commit/0c7e0f9b65dc0b2189c302065cdebdc2489ea842))
* add sphinx-based documentation ([#30](https://www.github.com/bihealth/clinvar-this/issues/30)) ([#31](https://www.github.com/bihealth/clinvar-this/issues/31)) ([d10adc5](https://www.github.com/bihealth/clinvar-this/commit/d10adc50a720548b580b7aa6bd52477012bb6d29))
* add tests for submission messages ([#19](https://www.github.com/bihealth/clinvar-this/issues/19)) ([#22](https://www.github.com/bihealth/clinvar-this/issues/22)) ([b168d47](https://www.github.com/bihealth/clinvar-this/commit/b168d47e0b3aed8d3a706ddbd28ddbb635ad86b4))
* add unit tests for submission messages ([#19](https://www.github.com/bihealth/clinvar-this/issues/19)) ([#20](https://www.github.com/bihealth/clinvar-this/issues/20)) ([1c4e11a](https://www.github.com/bihealth/clinvar-this/commit/1c4e11aa6eda5ebce0a66e8f21f17ea89c7ed7e2))
* adding mypy type checking ([#11](https://www.github.com/bihealth/clinvar-this/issues/11)) ([#12](https://www.github.com/bihealth/clinvar-this/issues/12)) ([700994a](https://www.github.com/bihealth/clinvar-this/commit/700994a113f2441bba76e3dc95adccf9fed6a156))
* adjust to ClinVar API change (Nov 2022) ([#47](https://www.github.com/bihealth/clinvar-this/issues/47)) ([#48](https://www.github.com/bihealth/clinvar-this/issues/48)) ([0e4fb50](https://www.github.com/bihealth/clinvar-this/commit/0e4fb508bda571c0c0afdab417e9052667f46ea1))
* allow annotation with HPO terms in TSV format ([#50](https://www.github.com/bihealth/clinvar-this/issues/50)) ([#56](https://www.github.com/bihealth/clinvar-this/issues/56)) ([0b0da41](https://www.github.com/bihealth/clinvar-this/commit/0b0da41e938e464e97ea1be7edcad6c666860f1e))
* allow import of extra columns ([#53](https://www.github.com/bihealth/clinvar-this/issues/53)) ([#54](https://www.github.com/bihealth/clinvar-this/issues/54)) ([616bfe7](https://www.github.com/bihealth/clinvar-this/commit/616bfe7867fe7ddd1c898f7582b1a353069b7ccd))
* completing enums ([#23](https://www.github.com/bihealth/clinvar-this/issues/23)) ([#24](https://www.github.com/bihealth/clinvar-this/issues/24)) ([9198983](https://www.github.com/bihealth/clinvar-this/commit/919898305a6155408118cd43a982c78153976879))
* implement api models ([#4](https://www.github.com/bihealth/clinvar-this/issues/4)) ([#5](https://www.github.com/bihealth/clinvar-this/issues/5)) ([3690c36](https://www.github.com/bihealth/clinvar-this/commit/3690c36b25fc98e520a401f8755a48b3451a972f))
* implement attrs-based message models ([#1](https://www.github.com/bihealth/clinvar-this/issues/1)) ([#2](https://www.github.com/bihealth/clinvar-this/issues/2)) ([f253c24](https://www.github.com/bihealth/clinvar-this/commit/f253c248cf35f749ace3c68633eb8d0357349688))
* implement enums for submission messages ([#14](https://www.github.com/bihealth/clinvar-this/issues/14)) ([#16](https://www.github.com/bihealth/clinvar-this/issues/16)) ([201cbe4](https://www.github.com/bihealth/clinvar-this/commit/201cbe4e055e0d013efe6f85a91b5ec339c77838))
* implement internal models for submissions ([#9](https://www.github.com/bihealth/clinvar-this/issues/9)) ([#26](https://www.github.com/bihealth/clinvar-this/issues/26)) ([be04e40](https://www.github.com/bihealth/clinvar-this/commit/be04e40e15adba180827fdc808c17d7d1647edb7))
* implement minimal TSV format ([#17](https://www.github.com/bihealth/clinvar-this/issues/17)) ([#18](https://www.github.com/bihealth/clinvar-this/issues/18)) ([960827d](https://www.github.com/bihealth/clinvar-this/commit/960827d9be757e5cc1cfe537451e3a34c738b256))
* implement models for extra files ([#6](https://www.github.com/bihealth/clinvar-this/issues/6)) ([#13](https://www.github.com/bihealth/clinvar-this/issues/13)) ([852e4c6](https://www.github.com/bihealth/clinvar-this/commit/852e4c6cd981ae533afbfda0217a4b9e1de8065e))
* implement models for submission message ([#8](https://www.github.com/bihealth/clinvar-this/issues/8)) ([#15](https://www.github.com/bihealth/clinvar-this/issues/15)) ([90afd10](https://www.github.com/bihealth/clinvar-this/commit/90afd105fc0d29c3962529157f38a20e48090a56))
* implement more columns in TSV ([#39](https://www.github.com/bihealth/clinvar-this/issues/39)) ([#55](https://www.github.com/bihealth/clinvar-this/issues/55)) ([6184d76](https://www.github.com/bihealth/clinvar-this/commit/6184d76a2f8261131718bbe69e88fdaf66b3a8de))
* implementing REST clinvar_api.client module ([#28](https://www.github.com/bihealth/clinvar-this/issues/28)) ([#29](https://www.github.com/bihealth/clinvar-this/issues/29)) ([829d907](https://www.github.com/bihealth/clinvar-this/commit/829d907763db617a04d277f297256980d25d51ab))
* store errors from "batch retrieve" ([#59](https://www.github.com/bihealth/clinvar-this/issues/59)) ([#60](https://www.github.com/bihealth/clinvar-this/issues/60)) ([67b8b0c](https://www.github.com/bihealth/clinvar-this/commit/67b8b0ccd85d4a913e7b8f1eb30dc4e96a2af32c))
* write data into profile sub directory ([#52](https://www.github.com/bihealth/clinvar-this/issues/52)) ([e699736](https://www.github.com/bihealth/clinvar-this/commit/e6997367d77586c1337a44fa7b5306ecede52a41))


### Bug Fixes

* interpret TSV OMIM "not provided" ([#57](https://www.github.com/bihealth/clinvar-this/issues/57)) ([#58](https://www.github.com/bihealth/clinvar-this/issues/58)) ([b655097](https://www.github.com/bihealth/clinvar-this/commit/b655097f2bf534b57115e3f9f5d18387ddfb1f18))


### Documentation

* add getting started tutorial to README ([#45](https://www.github.com/bihealth/clinvar-this/issues/45)) ([#61](https://www.github.com/bihealth/clinvar-this/issues/61)) ([3de084b](https://www.github.com/bihealth/clinvar-this/commit/3de084b49c184dfc6fb977b64cf478f03275ef9b))
