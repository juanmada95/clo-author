# power_sensitivity_table.R
# Generates power_sensitivity_table.csv (OSF deposit artifact, PAP §3.5 / item C10).
#
# Implements the pre-registered McNemar paired-proportions formula:
#   n = (z_alpha/2 + z_beta)^2 * p_d * (1 - p_d) / (p2 - p1)^2
#
# Sensitivity grid pre-registered in PAP §3.5:
#   discordant-pair rate p_d in {0.20, 0.30, 0.40}
#   detectable difference (p2 - p1) in {0.05, 0.10, 0.15}
#
# Constants:
#   alpha = 0.05 two-sided  -> z_alpha/2 = qnorm(0.975)
#   power = 0.80            -> z_beta    = qnorm(0.80)

# ---- Output path ----------------------------------------------------------
output_dir  <- file.path("quality_reports", "strategy", "cdd_formacion_inicial")
output_file <- file.path(output_dir, "power_sensitivity_table.csv")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

# ---- Pre-registered constants ---------------------------------------------
alpha   <- 0.05
power   <- 0.80
z_alpha <- qnorm(1 - alpha / 2)   # 1.959964
z_beta  <- qnorm(power)           # 0.8416212
zsum_sq <- (z_alpha + z_beta)^2

# ---- Sensitivity grid -----------------------------------------------------
grid <- expand.grid(
  p_d  = c(0.20, 0.30, 0.40),
  diff = c(0.05, 0.10, 0.15)
)

grid$n_pairs_required <- ceiling(
  zsum_sq * grid$p_d * (1 - grid$p_d) / grid$diff^2
)

grid <- grid[order(grid$p_d, grid$diff), ]
grid$alpha_two_sided <- alpha
grid$power           <- power
grid$z_alpha_half    <- round(z_alpha, 4)
grid$z_beta          <- round(z_beta,  4)

grid <- grid[, c("p_d", "diff", "alpha_two_sided", "power",
                 "z_alpha_half", "z_beta", "n_pairs_required")]

# ---- Write deposit artifact -----------------------------------------------
write.csv(grid, output_file, row.names = FALSE)
cat("Wrote", output_file, "\n")
print(grid)
