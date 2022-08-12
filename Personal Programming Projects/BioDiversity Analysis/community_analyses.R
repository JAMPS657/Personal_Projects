# EBIO 4800- Microbial Ecology in Practice
# Adam J. Solon (your name)
# OCT 2020
# Initial Description of microbial communities of Llullaillaco and Socompa Volcanoes
#
# DNA-seq data= 18S (Eukaryotes)
#
#check and set working directory- WILL BE DIFFERENT FOR EACH USER
getwd()
setwd("C:/Users/adams/Desktop/EBIO4800_Microbial_Ecology/Bioinformatics")
getwd()

#install mctoolsr package- Microbial community analysis tools in R
#install.packages("devtools")
#devtools::install_github("leffj/mctoolsr")
#install.packages("vegan")
#install.packages("dunn.test")
#install.packages("ggpubr")
#install.packages("VennDiagram")
#install.packages("RVAideMemoire")
#install.packages("tidyverse")
#install.packages("agricolae")

#open package from library
library(mctoolsr)

#input data files
#combine the ESV table w/ taxonomy and the mapping(metadata) file
input <-  load_taxa_table("Praxis_soco_llul_esvtab_wTax_18s_mctoolsr.txt", "Praxis_soco_llul_map_file_18s_mctoolsr.txt")

#return numbers of sequences per sample
sort(colSums(input$data_loaded))

#rarefy (i.e. normalize for variable sequence depths) to XXXX sequences per sample
input_rar = single_rarefy(input, 6581)

#export as .txt file
#only for reference DO NOT do this step (had to make some changes to the .txt outside of R)
#export_taxa_table(input_rar, "Praxis_soco_llul_rarefied_esvtab_18s_export.txt")

#QUESTION: what microbes are found in each sample, habitat type, at each elevation?
#Summarize taxonomic relative abundances by taxonomic level: e.g. 2 = phylum, 3 = class, 4 = order, etc.
tax_sum_phyla = summarize_taxonomy(input_rar, level = 2, report_higher_tax = FALSE)

#show only 1st five rows in console
tax_sum_phyla[1:5, 1:8]

#show all rows in console
tax_sum_phyla

#save as .txt file for external use
export_taxa_table(tax_sum_phyla, "18s_phyla_summarize")

#Summarizd by family
tax_sum_families = summarize_taxonomy(input_rar, level = 5, report_higher_tax = FALSE)
tax_sum_families

#save as .txt file for external use
export_taxa_table(tax_sum_phyla, "18s_family_summarize")

#plot w/ a heatmap based on habitat type
#plot w/ a heatmap based on habitat type
plot_ts_heatmap(tax_sum_phyla, input_rar$map_loaded, 0.01, 'Habitat', custom_sample_order = c('Fumarole', 'Penitentes', 'Dry'))

plot_ts_heatmap(tax_sum_families, input_rar$map_loaded, 0.01, 'Habitat', custom_sample_order = c('Fumarole', 'Penitentes', 'Dry'))

#plot w/ a heatmap based on elevation
plot_ts_heatmap(tax_sum_phyla, input_rar$map_loaded, 0.01, 'Elevation_masl', custom_sample_order = c('5825', '6049', '5100', '5277', '5300', '5650'))

#QUESTION: Are there differences in ESV richness levels between habitat types?
#ALPHA Diversity
#plot ESV richness levels by habitat type
plot_diversity(input_rar, "Habitat", "richness")

#QUESTION: Are there difference in community compositions between habitat types?
#BETA Diversity
#Calculate a dissimilarity matrix - default is Bray-Curtis
dm = calc_dm(input_rar$data_loaded)

#calculate a ordination for dissimilarity matrix- use Principal Coordinates Analysis (PCoA) option
ord = calc_ordination(dm, 'pcoa')  #other options include 'nmds'

#plot ordination on two axes - i.e. 'PCoA plot'
plot_ordination(input_rar, ord, 'Habitat', hulls = TRUE)

#statistical test- multivariate, non-parametric, null hypothesis signficance test
#Permutational Multivariate Analysis of Variance (PERMANOVA)- pairwise function from RVAideMemoire

#open package from library
library(RVAideMemoire)

#use pairwise permanova
pmanova <- pairwise.perm.manova(dm, input_rar$map_loaded$Habitat, nperm= 99)
pmanova

#save as .txt file for external use
cat(capture.output(print(pmanova), file="18s_BrayCurtis_pmanova.txt"))

#Question- Are there any taxa shared by all samples from each habitat?
core <- core_taxa(input_rar, "Habitat", prop_types = .35)
core

#save as .txt file for external use
cat(capture.output(print(core), file="18s_core_taxa_35perc.txt"))

#Question- Are there any taxa shared by samples from both elevations?
core1 <- core_taxa(input_rar, "Elevation_masl", prop_types = .35)
core1

#show numbers of ESVs shared between, and among, habitat types
plot_venn_diagram(input_rar, 'Habitat', pres_thresh = 0.01)

###recompute richness w/ different function in order to use statistical test
library(tidyverse)

#import non-mctoolsr format mapping file and esv table (no taxonomy)
#map file
map.alpha <- read.table("Praxis_soco_llul_map_file_18s_mctoolsr.txt", header = T, sep = "\t")

#ESV table
esvtab <- read.table("Praxis_soco_llul_rarefied_esvtab_18s_export.txt", header = T, sep = "\t")

#create data.frame of only taxonomy
taxonomy <- as.data.frame(esvtab$taxonomy)
rownames(taxonomy) <- esvtab$ESV_ID
names(taxonomy)[1] <- "taxonomy"

#set row names as ESV_ID column
rownames(esvtab) <- esvtab$ESV_ID

#remove ESV_ID' column and 'taxonomy' column from esvtab
esvtab$ESV_ID <- NULL
esvtab$taxonomy <- NULL

#use 'vegan' package to determine richness (i.e. number of ESVs)
library(vegan)

##calculate alpha diversity - species richness
richness <- as.data.frame(specnumber(t(esvtab)), MARGIN = 1) #margin is either number(1) or frequency(2) of species
richness

richness <- tibble::rownames_to_column(richness, "SampleID")

df <- merge(map.alpha, richness, by="SampleID", all=FALSE)

names(df)[10] <- "richness"

#save as .txt file
write.table(df, "18s_richness_vegan.txt", sep="\t", row.names=FALSE)

#boxplot of richness by habitat
pr <- ggplot(df, aes(x = Habitat, y = richness, color = Habitat)) + 
  geom_boxplot()+
  geom_jitter(shape=16, position=position_jitter(0.2))+
  ggtitle("Bacteria - Richness - # of ESVs") +
  xlab("Habitat") + ylab("ESV Richness")+
  labs(color = "Habitat")+
  theme_classic()

pr

#### parametric test
# ANOVA to test for differences
aov.richness <- aov(richness ~ Habitat, df)
summary(aov.richness)

#save as .txt file for external use
cat(capture.output(print(aov.richness), file="18s_richness_ANOVA.txt"))

#test for normality of data for determination of appropriate statistical test (i.e. parametric or non-parametric)
# visual determination- qqplot
#use 'ggpubr' package to display qq plot to check normality
library(ggpubr)

#plot residuals for to check normality
prqq <- ggqqplot(aov.richness$residuals)
prqq

#use 'agricolae' package for Tukey HSD test
library(agricolae)

#Tukeys pairwise
tuk.rich <- HSD.test(aov.richness, "Habitat", group = TRUE)
tuk.rich

#save as .txt file for external use
cat(capture.output(print(tuk.rich), file="soco_llul_18s_richness_TukeyHSD.txt"))

#save object w/ HSD signficance groups
tuk.rich.group <- tuk.rich$groups[order(rownames(tuk.rich$groups)),]

######boxplot of richness by location (i.e. Habitat type) w/ statistical significance groups
pr.s <- ggplot(df, aes(x = Habitat, y = richness, color = Habitat)) + 
  geom_text(data = data.frame(), #add the significance groupings from Tukey HSD output
            aes(x = rownames(tuk.rich.group), y = max(df$richness) + 1, label = tuk.rich.group$groups),
            col = 'black',
            size = 5) +
  geom_boxplot()+
  geom_jitter(shape=16, position=position_jitter(0.2))+ #geom_jitter shows the individual datapoints
  scale_x_discrete(limits=c("Fumarole", "Penitentes", "Dry")) + #scale_x_discrete rearranges the boxes in chosen order
  ggtitle("Bacteria - Richness - # of ESVs") +
  xlab("Habitat") + ylab("# of ESVs")+
  labs(color = "Habitat")+
  theme_classic()

pr.s
